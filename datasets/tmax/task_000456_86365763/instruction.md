You are tasked with building a robust, concurrent Configuration Manager system in Rust that tracks service changes, processes compressed configuration uploads, and migrates legacy data. 

**Stage 1: Information Extraction**
You have been provided with an image file at `/app/blueprint.png`. This image contains a scanned architectural blueprint for the new configuration manager. Use an OCR tool (like `tesseract`, which is installed) to read the text on this image. You will find an `API_TOKEN` and a `PORT` specification. You must use these exact values for the service you build in Stage 3.

**Stage 2: Legacy Migration (Metadata Search & Bulk Rename)**
There is a directory of legacy configuration files at `/app/legacy_configs/`. It contains hundreds of `.gz` files with arbitrary names (e.g., `conf_8821.gz`). 
Write a script or Rust program that:
1. Iterates over all `.gz` files in `/app/legacy_configs/`.
2. Decompresses each file to read the JSON metadata inside.
3. Each JSON file has the format: `{"service_name": "...", "version": 1, "settings": {...}}`.
4. Copies and renames the file to a new directory `/home/user/active_configs/` using the naming convention: `<service_name>_v<version>.json.gz`. 
5. Ensure the new file remains validly gzip-compressed.

**Stage 3: The Rust Configuration Daemon**
Create a Rust project at `/home/user/config_daemon`. Build an HTTP service (using `axum`, `actix-web`, or `hyper`—your choice) that does the following:
1. Listens on `127.0.0.1:<PORT>` (using the port from the blueprint).
2. Provides a `POST /upload` endpoint.
   - **Authentication**: Must require an `Authorization: Bearer <API_TOKEN>` header (using the token from the blueprint). Return `401 Unauthorized` if missing or incorrect.
   - **Payload**: The request body will be a gzip-compressed JSON payload containing `{"service_name": "...", "version": <number>, "settings": {...}}`.
   - **Processing**: 
     - Decompress the incoming streaming payload.
     - Parse the JSON to extract the `service_name` and `version`.
     - Write the compressed stream to `/home/user/active_configs/<service_name>_v<version>.json.gz`.
   - **Concurrency & Locking**: 
     - Upon a successful save, the service must append a line to `/home/user/system_changelog.log` in the exact format: `UPDATED <service_name> TO v<version>\n`.
     - Because multiple requests might arrive concurrently, you **must** use OS-level file locking (e.g., via the `fs3` or `fd-lock` crate) to acquire an exclusive lock on `/home/user/system_changelog.log` before appending to it, ensuring no interleaved writes occur.
   - Return a `200 OK` on success.

Start the Rust service in the background and leave it running.

**Final Deliverables Check:**
1. `/home/user/active_configs/` populated with renamed legacy files.
2. The Rust service running on the correct port and correctly authenticating requests.
3. The Rust service gracefully handling concurrent uploads and locking the changelog.