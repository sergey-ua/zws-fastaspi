package zws.database.repositories;

import zws.database.models.visit_model.VisitModel;
import sqlalchemy.orm.Session;
import sqlalchemy.exc.SQLAlchemyError;

public class VisitRepository {

    private final Session session;

    public VisitRepository(Session session) {
        this.session = session;
    }

    public void trackVisit(String urlShortBase64) {
        if (urlShortBase64 == null || urlShortBase64.isEmpty()) {
            throw new IllegalArgumentException("urlShortBase64 cannot be null or empty");
        }

        VisitModel visit = new VisitModel();
        visit.setUrlShortBase64(urlShortBase64);
        visit.setTimestamp(new java.sql.Timestamp(System.currentTimeMillis()));

        try {
            session.add(visit);
            session.commit();
        } catch (SQLAlchemyError e) {
            session.rollback();
            throw e;
        } finally {
            session.close();
        }
    }
}