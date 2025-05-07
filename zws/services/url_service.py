package zws.services;

import zws.database.repositories.url_repository.UrlRepository;
import java.util.UUID;
import java.net.URL;
import java.net.MalformedURLException;

public class UrlService {
    private final UrlRepository urlRepository;

    public UrlService(UrlRepository urlRepository) {
        this.urlRepository = urlRepository;
    }

    public String[] shortenUrl(String url) throws Exception {
        validateUrl(url);
        String shortIdentifier;
        int maxAttempts = 10;
        int attempts = 0;

        do {
            if (attempts >= maxAttempts) {
                throw new Exception("Failed to generate a unique short identifier after maximum attempts.");
            }
            shortIdentifier = generateUniqueIdentifier();
            attempts++;
        } while (!urlRepository.isShortUnique(shortIdentifier));

        urlRepository.create(shortIdentifier, url);
        return new String[]{shortIdentifier, url};
    }

    public String getOriginalUrl(String shortIdentifier) throws Exception {
        String originalUrl = urlRepository.getByShort(shortIdentifier);
        if (originalUrl == null) {
            throw new Exception("No URL found for the provided short identifier.");
        }
        return originalUrl;
    }

    private void validateUrl(String url) throws MalformedURLException {
        new URL(url);
    }

    private String generateUniqueIdentifier() {
        return UUID.randomUUID().toString().substring(0, 8);
    }
}