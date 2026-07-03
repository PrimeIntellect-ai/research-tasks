You are acting as a backup administrator managing an automated data archiving system. We have a set of legacy services running in `/app/` that process incoming data exports, but the pipeline is currently incomplete and the API is broken.

Here is the current state of the system:
1.  **Incoming Data**: There is a directory at `/app/data/incoming/` containing various files.
2.  **Redis Cache**: A Redis server is running locally on port 6379.
3.  **Manifest API**: A broken Flask application is located at `/app/api/app.py`, intended to run on port 5000.

Your objective is to complete the archiving pipeline by performing the following steps:

**Phase 1: File Search and Transformation**
1. Find all `.json` and `.csv` files in `/app/data/incoming/` that contain the word "CONFIDENTIAL" anywhere in their file contents. 
2. For each matching file, you must apply a redaction rule and save the cleaned version to `/app/data/archive/` (keep the original filename):
   - For `.json` files: Parse the JSON. If there is an `email` key at the root level, change its value to exactly `[REDACTED]`. Save the modified JSON.
   - For `.csv` files: The CSV has no header. If the second column looks like an email address (contains an `@`), replace the entire column value with `[REDACTED]`. Keep the rest of the row intact. Save the modified CSV.

**Phase 2: Checksum Generation & Metadata Storage**
1. For every file you successfully archived into `/app/data/archive/`, calculate its SHA-256 checksum.
2. Store this mapping in the local Redis instance (port 6379). Use a Redis Hash named `archive_manifest`. The field name should be the base filename (e.g., `data1.json`), and the value should be its SHA-256 checksum.

**Phase 3: Manifest API Configuration**
1. The Flask app at `/app/api/app.py` is missing the logic to connect to Redis and serve the manifest. Modify the code using Python so that it:
   - Listens on `127.0.0.1:5000`.
   - Exposes a `GET /manifest` endpoint.
   - Returns a JSON response containing the exact contents of the `archive_manifest` Redis hash (i.e., a JSON object where keys are filenames and values are SHA-256 checksums).
2. Start the Flask application in the background so it is actively serving requests on port 5000.

Ensure your Python script runs reliably, the transformed files are strictly formatted, and the Flask service is actively listening on port 5000 before you finish.