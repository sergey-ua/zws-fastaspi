package zws.services;

import zws.database.repositories.shortened_url_repository.ShortenedUrlRepository;
import zws.database.models.shortened_url.ShortenedUrl;
import zws.database.models.visit.Visit;
import zws.services.blocked_hostnames_service.BlockedHostnamesService;
import sqlalchemy.orm.Session;
import sqlalchemy.exc.SQLAlchemyError;
import secrets;
import urllib.parse.urlparse;
import datetime.datetime;

public class ShortenedUrlService {

    private final ShortenedUrlRepository shortenedUrlRepository;
    private final BlockedHostnamesService blockedHostnamesService;

    public ShortenedUrlService(ShortenedUrlRepository shortenedUrlRepository, BlockedHostnamesService blockedHostnamesService) {
        this.shortenedUrlRepository = shortenedUrlRepository;
        this.blockedHostnamesService = blockedHostnamesService;
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

        return "https://short.url/" + shortId;
    }

    private String generateUniqueShortId() throws Exception {
        int maxAttempts = 10;
        for (int i = 0; i < maxAttempts; i++) {
            String shortId = secrets.token_urlsafe(6);
            if (shortenedUrlRepository.isShortIdUnique(shortId)) {
                return shortId;
            }
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
        return result;
    }

    public void trackUrlVisit(String shortId) throws Exception {
        validateShort(shortId);

        ShortenedUrl record = shortenedUrlRepository.getByShortId(shortId);
        if (record == null) {
            throw new ValueError("URL not found");
        }

        try (Session session = shortenedUrlRepository.getSession()) {
            Visit visit = new Visit();
            visit.setTimestamp(datetime.datetime.now());
            visit.setShortenedUrlId(record.getId());
            session.beginTransaction();
            session.persist(visit);
            session.getTransaction().commit();
        } catch (SQLAlchemyError e) {
            throw new RuntimeException("Failed to log visit", e);
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