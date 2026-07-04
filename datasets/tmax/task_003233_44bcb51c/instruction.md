You are tasked with normalizing an archive of legacy configuration files and serving them via a new configuration management endpoint.

You have been provided with an image containing the new server specifications at `/app/server_spec.png`. You must use OCR (e.g., `tesseract`) to extract the port number and the new secret token from this image.

Additionally, there is an archive of legacy configurations at `/app/configs.tar.gz`. Extract it to a temporary location. The files inside have inconsistent casing, various extensions, and use different character encodings.

Perform the following operations:
1. Create a directory named `/app/processed/`.
2. For every file extracted from the archive:
   - Convert its character encoding to UTF-8.
   - Rename the file so its entire name is lowercase, and change its extension to `.conf` (e.g., `WEBSERVER.cfg` becomes `webserver.conf`).
   - Replace all occurrences of the literal string `REPLACE_ME_TOKEN` with the secret token you extracted from the image.
   - Save the transformed file into `/app/processed/`.

Once the files are processed, write and run a Python script that starts an HTTP server listening on `0.0.0.0` at the port specified in the image. This server must serve the static files from the `/app/processed/` directory.

Leave the server running in the background or foreground so that the system can verify the configuration files via HTTP GET requests.