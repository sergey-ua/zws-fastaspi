package zws.database.repositories;

import sqlalchemy.orm.Session;
import sqlalchemy.exc.IntegrityError;
import zws.database.models.shortened_url.ShortenedUrlModel;

import java.util.List;

public class ShortenedUrlRepository {

    public void createShortenedUrl(Session session, String short, String url, java.time.LocalDateTime createdAt) {
        try (session) {
            session.beginTransaction();
            ShortenedUrlModel shortenedUrl = new ShortenedUrlModel();
            shortenedUrl.setShort(short);
            shortenedUrl.setUrl(url);
            shortenedUrl.setCreatedAt(createdAt);
            session.persist(shortenedUrl);
            session.getTransaction().commit();
        } catch (IntegrityError e) {
            if (session.getTransaction().isActive()) {
                session.getTransaction().rollback();
            }
            throw e;
        } catch (Exception e) {
            if (session.getTransaction().isActive()) {
                session.getTransaction().rollback();
            }
            throw e;
        }
    }

    public ShortenedUrlModel getShortenedUrlByShort(Session session, String short) {
        try (session) {
            return session.createQuery("FROM ShortenedUrlModel WHERE short = :short", ShortenedUrlModel.class)
                          .setParameter("short", short)
                          .uniqueResult();
        }
    }

    public List<ShortenedUrlModel> getAllShortenedUrls(Session session) {
        try (session) {
            return session.createQuery("FROM ShortenedUrlModel", ShortenedUrlModel.class).list();
        }
    }
}