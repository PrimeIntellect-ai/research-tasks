You are a backup administrator tasked with finalizing our new distributed backup ingestion pipeline. The system receives backup archives (tar.gz files containing data files and an `index.xml` manifest) from remote clients, validates them, chunks the data, and stores them safely.

The system is located in `/home/user/backup_pipeline/` and consists of three cooperating services:
1. Nginx (Reverse Proxy)
2. Flask (Python Backend API)
3. Redis (Distributed Lock Manager)

Your tasks are as follows:

**Phase 1: Multi-Service Composition & Configuration**
1. The services are controlled via a startup script `/home/user/backup_pipeline/start_services.sh`. Nginx should listen on port 8080 and forward requests to the Flask app on `127.0.0.1:5000`. Edit the Nginx configuration at `/home/user/backup_pipeline/nginx.conf` to correctly proxy requests to the Flask application.
2. The Flask app (`/home/user/backup_pipeline/app.py`) currently fails because it does not properly establish a connection to Redis (listening on `127.0.0.1:6379`). Fix the Redis connection parameters in the Flask app. Ensure the app uses Redis to acquire a distributed lock (using the backup ID as the key) before writing any files to disk to prevent concurrent write corruption.

**Phase 2: Adversarial Backup Sanitization**
We frequently receive corrupted or malicious backup payloads. You must implement a strict validator in `/home/user/backup_pipeline/validator.py`.
The validator must expose a function `validate_backup(tar_path: str) -> bool`.
A backup is considered "evil" (return `False`) if:
- The `index.xml` manifest is missing or contains malformed XML.
- Any `<file>` tag in the XML manifest contains path traversal sequences (e.g., `../`, `..%2f`, absolute paths starting with `/`).
- The archive contains files not listed in the manifest, or the manifest lists files not present in the archive.
- The decompressed size of any file exceeds 5MB (Zip bomb prevention).

A backup is "clean" (return `True`) if it strictly adheres to the format without any of the above violations. 
We have provided test corpora in `/home/user/corpora/clean/` and `/home/user/corpora/evil/`. Your validator must reject 100% of the evil corpus and accept 100% of the clean corpus.

**Phase 3: Archiving and Format Transformation**
Update the Flask application (`app.py`) so that when a valid backup is received and locked:
1. Extract the tar.gz contents to a temporary directory.
2. Convert the `index.xml` manifest into a structured JSON file named `manifest.json`.
3. Split all extracted data files into 100KB chunks. 
4. Bulk rename the chunks using the format `<original_filename>.chunk.<4-digit-sequence>` (e.g., `database.db.chunk.0001`).
5. Move the `manifest.json` and all chunked files to `/home/user/archive/<backup_id>/`.

To test your end-to-end flow, start the services using the provided bash script, and ensure that sending a valid tar.gz via `curl -X POST -F "file=@/home/user/corpora/clean/test1.tar.gz" http://localhost:8080/upload` results in the correctly chunked files appearing in the archive directory.