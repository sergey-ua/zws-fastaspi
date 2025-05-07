package zws.database.repositories;

import sqlalchemy.orm.Session;
import sqlalchemy.exc.IntegrityError;
import zws.database.models.shortened_url.ShortenedUrlModel;

import java.time.LocalDateTime;
import java.time.format.DateTimeParseException;

public class ShortenedUrlRepository {

    public void insertUrlMapping(Session session, String url, String shortId, String createdAt) throws DuplicateShortIdException {
        try {
            LocalDateTime timestamp;
            try {
                timestamp = LocalDateTime.parse(createdAt);
            } catch (DateTimeParseException e) {
                throw new IllegalArgumentException("Invalid timestamp format for createdAt.");
            }

            ShortenedUrlModel shortenedUrl = new ShortenedUrlModel();
            shortenedUrl.setUrl(url);
            shortenedUrl.setShortId(shortId);
            shortenedUrl.setCreatedAt(timestamp);
            session.add(shortenedUrl);
            session.commit();
        } catch (IntegrityError e) {
            session.rollback();
            throw new DuplicateShortIdException("Duplicate short ID detected.");
        }
    }

    public boolean isHostnameBlocked(Session session, String hostname) {
        try {
            return session.query(ShortenedUrlModel.class)
                          .filterBy("hostname", hostname)
                          .first() != null;
        } catch (Exception e) {
            session.rollback();
            throw new RuntimeException("Error checking if hostname is blocked.", e);
        }
    }
}

class DuplicateShortIdException extends Exception {
    public DuplicateShortIdException(String message) {
        super(message);
    }
}