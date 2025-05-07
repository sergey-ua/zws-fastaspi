package zws.database.repositories;

import sqlalchemy.orm.Session;
import sqlalchemy.exc.SQLAlchemyError;
import zws.database.models.url_model.UrlModel;

public class UrlRepository {

    private final Session session;

    public UrlRepository(Session session) {
        this.session = session;
    }

    public UrlModel getUrlByShortBase64(String shortBase64) {
        try {
            return session.query(UrlModel.class)
                          .filter(UrlModel.shortBase64.eq(shortBase64))
                          .one_or_none();
        } catch (SQLAlchemyError e) {
            throw new RuntimeException("Error fetching URL by shortBase64", e);
        } finally {
            session.close();
        }
    }

    public void updateBlockedStatus(String shortBase64, boolean blocked) {
        try {
            UrlModel url = session.query(UrlModel.class)
                                  .filter(UrlModel.shortBase64.eq(shortBase64))
                                  .one_or_none();
            if (url == null) {
                throw new RuntimeException("URL not found for shortBase64: " + shortBase64);
            }
            url.setBlocked(blocked);
            session.commit();
        } catch (SQLAlchemyError e) {
            session.rollback();
            throw new RuntimeException("Error updating blocked status", e);
        } finally {
            session.close();
        }
    }
}