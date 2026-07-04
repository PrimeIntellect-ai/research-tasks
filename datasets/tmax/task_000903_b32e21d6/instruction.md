You are an AI assistant tasked with fixing and completing a configuration management system backed by an append-only Write-Ahead Log (WAL) and tarball archives. 

A partially implemented Python web service is vendored at `/app/wal-config-server`. This service acts as a configuration manager that tracks changes using a WAL file and creates compressed snapshots.

However, the package is broken, and its core file operations logic is incomplete.

Your task is to:

1. **Fix the Package Setup:**
   The package has a `Makefile` used to build and install the service, but it contains a deliberate error preventing `make install` from succeeding. Identify and fix the perturbation in the `Makefile` or `setup.py`/`requirements.txt` so you can install the dependencies and the package itself into your Python environment.

2. **Complete the Server Logic (`/app/wal-config-server/wal_server.py`):**
   The server exposes two HTTP endpoints that you must implement correctly using FastAPI or Flask (whichever is in the source):
   
   - **POST `/append`**: 
     Accepts raw binary data representing a configuration key-value pair. 
     *Requirement*: The incoming payload is encoded in `CP1252`. You must decode it, convert it to strict `UTF-8`, and append it to the WAL file located at `/app/data/config.wal`. The WAL format should be one JSON object per line: `{"key": "...", "value": "..."}`.
     
   - **POST `/commit`**:
     *Requirement*: 
     a) Parse `/app/data/config.wal`.
     b) Consolidate the keys (later entries overwrite earlier ones).
     c) Atomically write the consolidated JSON dictionary to a temporary file, then move it to `/app/data/snapshot.json`.
     d) Create a gzip-compressed tar archive named `/app/data/snapshot_<unix_timestamp>.tar.gz` containing `snapshot.json`.
     e) Create or update a **symbolic link** at `/app/data/current.tar.gz` pointing to the newly created archive.
     f) Clear the WAL file after a successful commit.

3. **Start the Service:**
   Run the fixed service such that it listens on `127.0.0.1:9090`. Keep it running in the background.

**Constraints & Specifications:**
- All files must be created within `/app/data/` (create the directory if it doesn't exist).
- The service must return HTTP 200 on success for both endpoints.
- You must use atomic file operations (e.g., write to a `.tmp` file and rename) when generating `snapshot.json`.
- The final archive must contain exactly one file named `snapshot.json`.