You are tasked with building a file processing and backup archiving service for our system. As a backup administrator, you need to handle incoming Write-Ahead Log (WAL) archives dropped into a specific directory, while also providing metadata about a surveillance video file.

Please write and start a Python HTTP service that listens on `0.0.0.0:8080`. The service must fulfill the following requirements:

1. **Video Analysis Endpoint**:
   - Implement a `GET /video_info` endpoint.
   - When called, the service must inspect the video file located at `/app/surveillance.mp4`.
   - It should calculate the exact total number of frames in the video.
   - Return a JSON response: `{"total_frames": <integer>}` with a 200 OK status.

2. **Incoming Archive Watcher (Background Task)**:
   - Your service must continuously monitor the directory `/app/incoming/` for new `.tar.gz` files using a file-watching mechanism (e.g., the `watchdog` library).
   - When a `.tar.gz` file is completely written and appears in the directory, verify its archive integrity and extract its contents to a temporary location.
   - The archive will contain one or more `.wal` files.
   - You must parse and validate each `.wal` file. A valid WAL file has the following format:
     - The first line is exactly `MAGIC_WAL`.
     - Followed by zero or more lines of transaction data.
     - The final line is exactly `END <md5_hash>`, where `<md5_hash>` is the MD5 hex digest of all preceding bytes in the file (up to and including the newline character immediately before the `END` line).
   - If a `.wal` file is valid, you must rename it by appending `_verified` to its base name (e.g., `db1.wal` becomes `db1_verified.wal`) and move it to `/app/archive/`.
   - If it is invalid (corrupt archive, invalid magic, or mismatched hash), discard it.

3. **Archive Status Endpoint**:
   - Implement a `GET /archived_wals` endpoint.
   - It must return a JSON response containing the list of verified WAL files currently in the `/app/archive/` directory, sorted alphabetically: `{"files": ["db1_verified.wal", "db2_verified.wal", ...]}`.

**Constraints & Setup**:
- Ensure all directories exist (`/app/incoming/`, `/app/archive/`).
- Your HTTP server must run continuously. Do not exit after processing.
- You may use standard libraries and any necessary PyPI packages (e.g., `Flask`, `FastAPI`, `watchdog`, `opencv-python`). You are responsible for installing them.

Start the service so that we can run our automated tests against port 8080.