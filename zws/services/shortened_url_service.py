package zws.services;

import zws.database.repositories.shortened_url_repository.ShortenedUrlRepository;
import zws.database.models.shortened_url.ShortenedUrl;
import zws.database.models.visit.Visit;
import zws.services.blocked_hostnames_service.BlockedHostnamesService;
import sqlalchemy.orm.Session;
import sqlalchemy.exc.SQLAlchemyError;
import secrets;
import base64;
import urllib.parse.urlparse;
import datetime.datetime;

public class ShortenedUrlService {

    private final ShortenedUrlRepository shortenedUrlRepository;
    private final BlockedHostnamesService blockedHostnamesService;
    private final String baseUrl;
    private static final int MAX_SHORT_ID_GENERATION_ATTEMPTS = 10;

    public ShortenedUrlService(ShortenedUrlRepository shortenedUrlRepository, BlockedHostnamesService blockedHostnamesService, String baseUrl) {
        this.shortenedUrlRepository = shortenedUrlRepository;
        this.blockedHostnamesService = blockedHostnamesService;
        this.baseUrl = baseUrl;
    }

    public String shortenUrl(String originalUrl) throws Exception {
        String parsedUrl = urlparse(originalUrl).getHost();
        if (parsedUrl == null || parsedUrl.isEmpty()) {
            throw new ValueError("Invalid URL format");
        }

        if (isUrlBlocked(originalUrl)) {
            throw new BlockedUrlException("That URL hostname is blocked");
        }

        String shortId = generateUniqueShortId();
        shortenedUrlRepository.createShortenedUrl(originalUrl, shortId);

        return baseUrl + "/" + shortId;
    }

    private String generateUniqueShortId() throws Exception {
        int attempts = 0;
        while (attempts < MAX_SHORT_ID_GENERATION_ATTEMPTS) {
            String shortId = secrets.token_urlsafe(6);
            if (shortenedUrlRepository.isShortIdUnique(shortId)) {
                return shortId;
            }
            attempts++;
        }
        throw new IDGenerationException("Unable to generate a unique short ID within the max number of attempts");
    }

    public Map<String, Object> retrieveUrl(String shortId) throws Exception {
        validateShort(shortId);

        ShortenedUrl record = shortenedUrlRepository.getByShortId(shortId);
        if (record == null) {
            return null;
        }

        Map<String, Object> result = new HashMap<>();
        if (record.isBlocked()) {
            result.put("long_url", null);
            result.put("blocked", true);
        } else {
            result.put("long_url", record.getLongUrl());
            result.put("blocked", false);
        }

        if (!record.isBlocked() && isUrlBlocked(record.getLongUrl())) {
            updateBlockedStatus(shortId, true);
            result.put("long_url", null);
            result.put("blocked", true);
        }

        return result;
    }

    public void trackUrlVisit(String shortId) throws Exception {
        validateShort(shortId);

        ShortenedUrl record = shortenedUrlRepository.getByShortId(shortId);
        if (record == null) {
            throw new ValueError("URL not found");
        }

        Session session = null;
        try {
            session = shortenedUrlRepository.getSession();
            session.beginTransaction();
            Visit visit = new Visit();
            visit.setTimestamp(datetime.datetime.now());
            visit.setShortenedUrlId(record.getId());
            session.persist(visit);
            session.getTransaction().commit();
        } catch (SQLAlchemyError e) {
            if (session != null) {
                session.getTransaction().rollback();
            }
            throw new RuntimeException("Failed to log visit", e);
        } finally {
            if (session != null) {
                session.close();
            }
        }
    }

    public void updateBlockedStatus(String shortId, boolean blocked) throws Exception {
        validateShort(shortId);

        ShortenedUrl record = shortenedUrlRepository.getByShortId(shortId);
        if (record == null) {
            throw new ValueError("Invalid short ID");
        }

        shortenedUrlRepository.updateBlockedStatus(shortId, blocked);
    }

    private void validateShort(String shortId) throws Exception {
        if (shortId == null || !shortId.matches("^[a-zA-Z0-9_-]{6,}$")) {
            throw new ValueError("Invalid short ID format");
        }
    }

    private boolean isUrlBlocked(String url) throws Exception {
        String hostname = urlparse(url).getHost();
        if (hostname == null || hostname.isEmpty()) {
            throw new ValueError("Invalid URL format");
        }
        return blockedHostnamesService.isHostnameBlocked(hostname);
    }
}