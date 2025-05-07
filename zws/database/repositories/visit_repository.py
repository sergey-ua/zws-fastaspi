package zws.database.repositories;

import sqlalchemy.orm.Session;
import zws.database.models.visit_model.VisitModel;

public class VisitRepository {

    private final Session session;

    public VisitRepository(Session session) {
        this.session = session;
    }

    public void trackVisit(String urlShortBase64, java.sql.Timestamp timestamp) {
        if (urlShortBase64 == null || urlShortBase64.isEmpty()) {
            throw new IllegalArgumentException("urlShortBase64 cannot be null or empty");
        }
        if (timestamp == null) {
            throw new IllegalArgumentException("timestamp cannot be null");
        }

        VisitModel visit = new VisitModel();
        visit.setUrlShortBase64(urlShortBase64);
        visit.setTimestamp(timestamp);

        try {
            session.add(visit);
            session.commit();
        } catch (Exception e) {
            session.rollback();
            throw e;
        }
    }
}