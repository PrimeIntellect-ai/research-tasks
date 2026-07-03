You are an backend web developer working on a legacy C-based microservice that handles text encoding and decoding. The service has been crashing in production due to memory safety issues, and you need to fix it, extract a configuration secret from an image, and deploy the service locally.

Here is what you need to do:

1. **Extract the API Key**:
   There is an image file located at `/app/secret_config.png`. This image contains the production API key in the format `API_KEY: <key>`. Use an OCR tool (like `tesseract`, which is preinstalled) to extract the key. You will need to configure the server to require this exact key in the `Authorization: Bearer <key>` header for all protected endpoints.

2. **Fix the C Server**:
   The source code for the HTTP server is located at `/app/server.c`. It uses raw sockets to listen for HTTP requests. 
   There are two main bugs in the code:
   - A memory safety issue (buffer overflow/undefined behavior) in the `url_decode` function when handling `%` escapes.
   - An off-by-one memory allocation bug in the `base64_encode` function causing heap corruption.
   
   Fix these memory safety issues so the server runs reliably without crashing or leaking memory. You should create a test fixture or mock setup script in Python or C to test the encoding/decoding logic locally before starting the server.

3. **Compile and Run**:
   Compile the fixed server using `gcc -o /app/server /app/server.c`.
   Start the server. It must listen on `127.0.0.1:8080`.

4. **Service Endpoints**:
   The server must expose a `POST /process` endpoint.
   - It must accept `application/x-www-form-urlencoded` data with a `text` field (e.g., `text=Hello%20World%21`).
   - It must require the `Authorization: Bearer <key>` header using the key extracted from the image. If the auth header is missing or incorrect, return a `401 Unauthorized` HTTP response.
   - It must URL-decode the value of the `text` field, base64-encode the resulting bytes, and return the base64 string in the HTTP response body with a `200 OK` status.

Leave the server running in the background when you are finished. An automated verifier will make HTTP requests to `127.0.0.1:8080` to test the `/process` endpoint with various payloads and check for memory stability and correct encoding/decoding.