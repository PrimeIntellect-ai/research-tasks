You are a platform engineer tasked with migrating our internal build artifact registry to a high-performance, lightweight microservice written in C, placed behind a secure reverse proxy. 

Your goals are to set up the API, implement a checksum verification mechanism, configure the reverse proxy, and write a mock CI/CD script to interact with it.

**Step 1: Recover the Authorization Token**
Our legacy documentation has been lost, but we have an old architecture diagram located at `/app/arch_diagram.png`. 
Use an OCR tool (like `tesseract`, which you can install via `apt-get`) to read the text in this image. Somewhere in the text is a token in the format `CI_TOKEN: <TOKEN_STRING>`. Extract this `<TOKEN_STRING>`.

**Step 2: Build the Artifact Server in C**
Write a C web service in `/home/user/artifact_server.c`. You may use `libmicrohttpd` (installable via `apt-get install libmicrohttpd-dev`) or plain sockets.
*   The server must listen on `127.0.0.1:8080`.
*   It must expose exactly one endpoint: `POST /upload`.
*   It must check for the HTTP header `Authorization: Bearer <TOKEN_STRING>` (using the token you extracted). If the header is missing or incorrect, return HTTP 401 Unauthorized.
*   For a valid request, compute the standard CRC32 checksum (IEEE 802.3) of the raw binary payload (the request body).
*   Return an HTTP 200 OK response with the `Content-Type: application/json` and the following exact JSON body: `{"status": "success", "checksum": "<8-character-hex-lowercase-crc32>"}`.
*   Compile your code to `/home/user/artifact_server` and ensure it runs in the background.

**Step 3: Configure the Reverse Proxy**
Install `nginx`. Configure it to act as a reverse proxy for your C service.
*   Nginx must listen on `127.0.0.1:8000`.
*   It must proxy all requests for `/upload` to `http://127.0.0.1:8080/upload`.
*   **Security Constraint:** Nginx must *only* allow `POST` requests to `/upload`. Any other HTTP method (GET, PUT, etc.) must be intercepted by Nginx and rejected with an HTTP 405 Method Not Allowed before reaching the C server.
*   Start the Nginx service.

**Step 4: Create the CI/CD Upload Script**
Write a bash script at `/home/user/upload_artifact.sh`. 
*   It must take exactly one argument (the path to a file).
*   It must use `curl` to upload the file's contents via `POST` to `http://127.0.0.1:8000/upload`.
*   It must automatically include the correct `Authorization` header with the extracted token.

Ensure both Nginx and your compiled C server are running at the end of your interaction so they can be verified.