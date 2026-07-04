You are a storage administrator tasked with building a secure, automated archive extraction and analysis service to manage disk space and filter out malicious uploads. You must implement this service using Python.

Your tasks:

1. **Configuration Retrieval:**
   There is an image file located at `/app/server_config.png`. This image contains handwritten/typed configuration text. You must extract the text from this image (e.g., using `tesseract` which is pre-installed) to find the port number your service must listen on and the secret administrative token it must require. The image contains text in the format:
   `ListenPort: <port>`
   `AdminToken: <token>`

2. **Develop the Service:**
   Write and start a Python HTTP web server listening on `0.0.0.0` at the port extracted from the image. You may use standard libraries (`http.server`) or install frameworks like `Flask` or `FastAPI`.

3. **Implement the `/analyze` Endpoint:**
   Create an endpoint that accepts `POST` requests at `/analyze`.
   - **Authentication:** The endpoint must check for the `Authorization` header. It must exactly match `Bearer <AdminToken>` (using the token from the image). If missing or invalid, return HTTP 401.
   - **Payload:** The request body will contain the raw binary data of a ZIP archive.
   - **Security (Zip Slip Mitigation):** Before extracting, you must inspect the archive. If any file path within the archive attempts to traverse outside the target extraction directory (e.g., contains `../` or absolute paths resolving outside the target), you must completely reject the request and return HTTP 400.
   - **Safe Extraction:** If safe, extract the archive to `/app/safe_storage/`. Because this endpoint might be called concurrently by different automated systems, you MUST acquire an exclusive file lock on `/app/safe_storage/extraction.lock` before extracting, and release it afterward to prevent race conditions.
   - **Binary Header Analysis:** After extraction, recursively traverse all files in `/app/safe_storage/`. Read the first 4 bytes of each file to determine its true type (do not rely on file extensions). 
     - If the file's magic number indicates an ELF executable (the first 4 bytes are `\x7FELF`), delete the file immediately to save disk space and prevent malware execution.
   - **Response:** After processing, return HTTP 200. The response body must be a JSON object containing the total count of files successfully retained (non-ELF files) across all extractions so far: `{"retained_files": X}`.

Ensure your Python server is running in the background and listening before you finish the task. Do not stop the server, as it will be tested by an automated verifier.