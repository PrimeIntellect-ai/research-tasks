You are tasked with building a secure artifact repository manager in Python that curates binary and text archives while defending against common extraction vulnerabilities. 

Your lead engineer left an audio memo at `/app/secret_passphrase.wav` containing the authorization token for this service. You will need to transcribe or listen to this audio file to retrieve the passphrase.

Build and start a Python web server (you may use `flask`, `fastapi`, or the standard library) that listens exactly on `127.0.0.1:8000`. The server must implement the following endpoints:

1. **`POST /upload`**
   - **Authentication:** Must require the header `Authorization: Bearer <passphrase_from_audio>`. Return HTTP 401 if missing or incorrect.
   - **Payload:** Expects a `multipart/form-data` payload with a ZIP archive uploaded in the field named `archive`.
   - **Security (Zip Slip Prevention):** Inspect the contents of the ZIP file BEFORE extracting. If any file path in the archive attempts to traverse outside the target directory (e.g., contains `../` or is an absolute path like `/etc/passwd`), reject the entire upload immediately with an HTTP 400 status code and the JSON response `{"error": "Zip Slip detected"}`.
   - **Processing:** If the archive is safe, extract its contents to `/home/user/artifacts/`. 
   - **Incremental Manifest:** After extraction, you must update a centralized checksum manifest located at `/home/user/artifacts/manifest.csv`. The CSV must have the header `filename,sha256`. Calculate the SHA256 hash of all files currently in the `/home/user/artifacts/` directory (excluding the manifest itself) and write them to the CSV. If a file is overwritten by a new upload, its hash should be updated in the manifest.
   - **Response:** Return HTTP 200 and `{"status": "success"}`.

2. **`GET /manifest`**
   - **Authentication:** Same as above.
   - **Response:** Return HTTP 200 with the exact plaintext contents of `/home/user/artifacts/manifest.csv`.

Start your server in the background or leave it running in the terminal so that the automated test suite can interact with it. Ensure `/home/user/artifacts/` exists and is properly managed.