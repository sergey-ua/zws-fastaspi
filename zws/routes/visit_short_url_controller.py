package zws.routes;

import fastapi.APIRouter;
import fastapi.Response;
import fastapi.HTTPException;
import pydantic.BaseModel;
import zws.services.urls_service.UrlsService;

public class VisitShortUrlController {

    private final APIRouter router;
    private final UrlsService urlsService;

    public VisitShortUrlController(UrlsService urlsService) {
        this.router = new APIRouter();
        this.urlsService = urlsService;
        defineRoutes();
    }

    private void defineRoutes() {
        router.get("/{short}", this::visitShortUrl);
    }

    public void visitShortUrl(String shortUrl, boolean visit, Response response) {
        if (shortUrl == null || shortUrl.isEmpty()) {
            throw new HTTPException(400, "Invalid short URL");
        }

        String originalUrl = urlsService.retrieveUrl(shortUrl);
        if (originalUrl == null) {
            throw new HTTPException(404, "That shortened URL couldn't be found");
        }

        if (urlsService.isUrlBlocked(shortUrl)) {
            throw new HTTPException(410, "That URL is blocked and can't be accessed");
        }

        if (!visit) {
            response.json(Map.of("url", originalUrl));
            return;
        }

        urlsService.trackUrlVisit(shortUrl);
        response.redirect(originalUrl, 308);
    }

    public APIRouter getRouter() {
        return router;
    }
}