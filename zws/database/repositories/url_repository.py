package zws.database.repositories;

import zws.database.models.url_model.UrlModel;
import sqlalchemy.orm.Session;
import sqlalchemy.exc.IntegrityError;
import sqlalchemy.orm.exc.NoResultFound;
import sqlalchemy.orm.exc.MultipleResultsFound;

import java.time.LocalDateTime;
import java.util.Optional;

public class UrlRepository {

    private final Session session;

    public UrlRepository(Session session) {
        this.session = session;
    }

    public Optional<UrlModel> getUrlByShortBase64(String shortBase64) {
        try {
            return Optional.ofNullable(
                session.query(UrlModel.class)
                       .filter(UrlModel.shortBase64.eq(shortBase64))
                       .oneOrNone()
            );
        } catch (NoResultFound | MultipleResultsFound e) {
            return Optional.empty();
        } catch (Exception e) {
            throw new RuntimeException("Error fetching URL by shortBase64", e);
        }
    }

    public Optional<UrlModel> getByShort(String shortValue) {
        try {
            return Optional.ofNullable(
                session.query(UrlModel.class)
                       .filter(UrlModel.short.eq(shortValue))
                       .oneOrNone()
            );
        } catch (NoResultFound | MultipleResultsFound e) {
            return Optional.empty();
        } catch (Exception e) {
            throw new RuntimeException("Error fetching URL by short", e);
        }
    }

    public boolean isShortIdExists(String shortId) {
        try {
            return session.query(UrlModel.class)
                          .filter(UrlModel.shortId.eq(shortId))
                          .count() > 0;
        } catch (Exception e) {
            throw new RuntimeException("Error checking if shortId exists", e);
        }
    }

    public boolean isShortUnique(String shortValue) {
        try {
            return session.query(UrlModel.class)
                          .filter(UrlModel.short.eq(shortValue))
                          .count() == 0;
        } catch (Exception e) {
            throw new RuntimeException("Error checking if short is unique", e);
        }
    }

    public boolean isHostnameBlocked(String hostname) {
        try {
            return session.query(UrlModel.class)
                          .filter(UrlModel.hostname.eq(hostname))
                          .filter(UrlModel.blocked.eq(true))
                          .count() > 0;
        } catch (Exception e) {
            throw new RuntimeException("Error checking if hostname is blocked", e);
        }
    }

    public void createUrl(String shortBase64, String url, boolean blocked) {
        try {
            UrlModel newUrl = new UrlModel();
            newUrl.setShortBase64(shortBase64);
            newUrl.setUrl(url);
            newUrl.setBlocked(blocked);
            session.add(newUrl);
            session.commit();
        } catch (IntegrityError e) {
            session.rollback();
            throw new RuntimeException("Error creating URL, possible unique constraint violation", e);
        } catch (Exception e) {
            session.rollback();
            throw new RuntimeException("Error creating URL", e);
        }
    }

    public void create(String url, String shortValue) {
        try {
            UrlModel newUrl = new UrlModel();
            newUrl.setUrl(url);
            newUrl.setShort(shortValue);
            session.add(newUrl);
            session.commit();
        } catch (IntegrityError e) {
            session.rollback();
            throw new RuntimeException("Error creating URL, possible unique constraint violation", e);
        } catch (Exception e) {
            session.rollback();
            throw new RuntimeException("Error creating URL", e);
        }
    }

    public void insertUrlMapping(String longUrl, String shortId, LocalDateTime createdAt, boolean blocked) {
        try {
            UrlModel newUrl = new UrlModel();
            newUrl.setUrl(longUrl);
            newUrl.setShortId(shortId);
            newUrl.setCreatedAt(createdAt);
            newUrl.setBlocked(blocked);
            session.add(newUrl);
            session.commit();
        } catch (IntegrityError e) {
            session.rollback();
            throw new RuntimeException("Error inserting URL mapping, possible unique constraint violation", e);
        } catch (Exception e) {
            session.rollback();
            throw new RuntimeException("Error inserting URL mapping", e);
        }
    }

    public void updateBlockedStatus(String shortBase64, boolean blocked) {
        try {
            UrlModel url = session.query(UrlModel.class)
                                  .filter(UrlModel.shortBase64.eq(shortBase64))
                                  .oneOrNone();
            if (url == null) {
                throw new RuntimeException("URL not found for shortBase64: " + shortBase64);
            }
            url.setBlocked(blocked);
            session.commit();
        } catch (NoResultFound e) {
            throw new RuntimeException("No URL found for shortBase64: " + shortBase64, e);
        } catch (Exception e) {
            session.rollback();
            throw new RuntimeException("Error updating blocked status", e);
        }
    }
}