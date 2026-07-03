You are acting as a security auditor and software engineer. You need to build a secure, isolated text-redaction HTTP service in Python that processes sensitive receipts, enforces strict permissions, and blocks malicious intrusion attempts.

Your tasks are:

1. **Extract and Redact Data from an Image:**
   There is an image of a receipt located at `/app/secret_receipt.png`. Use OCR (e.g., `tesseract`, which is preinstalled) to extract the text from this image. 
   You must identify the 16-digit credit card number within the text (which may be formatted with dashes) and redact it to exactly `XXXX-XXXX-XXXX-XXXX`.

2. **Build a Secure HTTP Service:**
   Write and start a Python HTTP server (using `http.server` or a lightweight framework like `Flask`/`FastAPI`, though standard library is preferred to minimize dependencies) listening on `127.0.0.1` port `8080`.

   The server must implement the following endpoints and security controls:
   
   - **Authentication:** All endpoints must require an `Authorization` header with the exact value: `Bearer AUDITOR-TOKEN-992`. If missing or incorrect, return a `401 Unauthorized` status code.
   - **Content Security Policy (CSP):** Every successful response must include the HTTP header: `Content-Security-Policy: default-src 'self'`.
   - **Intrusion Detection (WAF):** Inspect all incoming POST payloads. If the payload contains the exact substrings `<script>` or `UNION SELECT` (case-sensitive), immediately return a `403 Forbidden` status code.
   
   **Endpoints:**
   - `GET /receipt`: Returns the fully extracted text of `/app/secret_receipt.png` with the credit card number redacted as specified above. Return it as plain text.
   - `POST /redact`: Accepts raw plain text in the request body. It must redact any 16-digit credit card numbers (ignoring dashes) to `XXXX-XXXX-XXXX-XXXX` and return the redacted plain text.

3. **Running the Service:**
   Start the service in the background so it runs continuously and binds to `127.0.0.1:8080`. Write your server code to `/app/secure_server.py` and ensure it runs successfully.

Do not use external web frameworks unless you install them yourself, but the Python standard library's `http.server` is perfectly sufficient. Leave the server running when you are finished.