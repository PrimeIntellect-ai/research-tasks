You are acting as an automated assistant for a technical writer who is organizing and publishing a legacy documentation archive.

Your task has three phases:

**Phase 1: Token Extraction (Image Processing)**
We have a scanned legacy document containing a critical authorization token at `/app/legacy_watermark.png`. 
You need to extract the alphanumeric string labeled "AUTH_TOKEN:" from this image (using OCR tools like `tesseract`, which is preinstalled). You will need this token to secure the API you build in Phase 3.

**Phase 2: Data Parsing & Sanitization**
There is a compressed archive of legacy logs and draft documentation located at `/app/docs_archive.tar.gz`.
1. Extract the contents without leaving unredacted files on the disk permanently. 
2. Sanitize the text streams: Find any occurrence of an SSN-like pattern (`SSN: ` followed by `XXX-XX-XXXX` format numbers) and replace the digits completely with `[REDACTED]`. Also, replace the exact string `STATUS: DRAFT` with `STATUS: ARCHIVED`.
3. Save the sanitized files into `/home/user/clean_docs/`. To prevent race conditions with a local indexer that monitors this directory, you must use atomic writes (e.g., write to a temporary file first, then rename it to the final filename in `/home/user/clean_docs/`).

**Phase 3: Service Deployment**
Create and start a Python HTTP service (you may use Flask, FastAPI, or the standard library) listening on `127.0.0.1:8080`.
The service must implement the following:
1. **Authentication:** All endpoints must require an `Authorization` header in the format: `Bearer <extracted_token_from_Phase_1>`. Return a 401 Unauthorized status if missing or incorrect.
2. **GET `/docs/<filename>`:** Returns the raw text of the requested sanitized file from `/home/user/clean_docs/<filename>`. Return 404 if the file does not exist.
3. **POST `/append_note`:** Accepts a JSON payload like `{"file": "filename.txt", "note": "Reviewed by agent"}`. It must safely append the note to the specified file in `/home/user/clean_docs/` as a new line. Since a background writer might also be appending logs, this endpoint must use file locking (`fcntl`) or safe atomic append operations to prevent data corruption.

Leave the Python server running in the background so it can be tested.