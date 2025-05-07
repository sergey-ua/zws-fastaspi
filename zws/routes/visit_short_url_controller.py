package zws.routes;

import fastapi.FastAPI;
import fastapi.APIRouter;
import fastapi.HTTPException;
import fastapi.responses.RedirectResponse;
import pydantic.BaseModel;
import zws.services.blocked_hostnames_service.BlockedHostnamesService;
import zws.database.models.url_model.URLModel;
import zws.database.models.visit_model.VisitModel;
import sqlalchemy.orm.Session;

import java.util.Optional;

public class VisitShortUrlController {

    private final APIRouter router;
    private final BlockedHostnamesService blockedHostnamesService;

    public VisitShortUrlController(BlockedHostnamesService blockedHostnamesService) {
        this.router = new APIRouter();
        this.blockedHostnamesService = blockedHostnamesService;
        defineRoutes();
    }

    private void defineRoutes() {
        router.get("/urls/{short}", this::visitShortUrl);
    }

    public void visitShortUrl(String shortUrl, Optional<Boolean> visit, Session session) {
        if (shortUrl == null || shortUrl.isEmpty()) {
            throw new HTTPException(400, "Invalid short URL");
        }

        String encodedId = blockedHostnamesService.toBase64(shortUrl);
        URLModel urlRecord = session.createQuery(
                "SELECT u FROM URLModel u WHERE u.shortBase64 = :encodedId", URLModel.class)
                .setParameter("encodedId", encodedId)
                .setMaxResults(1)
                .uniqueResult();

        if (urlRecord == null) {
            throw new HTTPException(404, "That shortened URL couldn't be found");
        }

        if (urlRecord.isBlocked()) {
            throw new HTTPException(410, "That URL is blocked and can't be accessed");
        }

        if (visit.orElse(true)) {
            blockedHostnamesService.trackUrlVisitAsync(shortUrl);
            throw new RedirectResponse(urlRecord.getUrl(), 308);
        } else {
            throw new HTTPException(200, Map.of("url", urlRecord.getUrl()));
        }
    }

    public APIRouter getRouter() {
        return router;
    }
}