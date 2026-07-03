You are tasked with building an internal microservice to process, organize, and validate legacy project archives uploaded by automated systems. The legacy systems sometimes generate malformed or unsafe archives, and their text encoding is outdated.

Please write and run a Python HTTP service listening on `127.0.0.1:8080` that fulfills the following requirements:

1. **Endpoint**: Provide a `POST` route at `/upload_project`. The request body will contain the raw bytes of a ZIP archive.
2. **Integrity and Security (Zip Slip protection)**:
   - Verify the archive is a valid ZIP file.
   - Inspect the archive for path traversal vulnerabilities (Zip Slip). If *any* file inside the archive resolves to a path outside of the target extraction directory (e.g., using `../`), your service must NOT extract anything. Instead, it must immediately return an HTTP `400 Bad Request` status with the exact JSON response: `{"error": "Invalid archive"}`.
3. **Extraction & Encoding Conversion**:
   - If the archive is safe, extract its contents to a temporary directory.
   - Locate the `manifest.json` file inside the extracted files (it will be in the root of the archive).
   - The legacy system encodes `manifest.json` in `Windows-1252`. Read the file and parse the JSON into a Python dictionary, converting it to standard UTF-8.
4. **Binary Processing via Standard Streams**:
   - We have provided a legacy proprietary validation tool at `/app/metadata_signer` (a stripped ELF binary).
   - Your service must pipe the newly UTF-8 encoded JSON string into the standard input of `/app/metadata_signer`.
   - The binary will output a single signature string on standard output. You must capture this stdout.
5. **Response Format**:
   - On success, return an HTTP `200 OK` status.
   - The response must be a JSON object with two keys:
     - `"manifest"`: The parsed JSON dictionary from the archive.
     - `"signature"`: The exact signature string outputted by `/app/metadata_signer` (strip any trailing newlines).

You may use standard libraries or install any common Python web frameworks (e.g., Flask, FastAPI) to build this service. Keep the service running in the foreground or background so it can be tested.