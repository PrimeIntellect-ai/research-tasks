You are tasked with optimizing and securing a multi-service backup ingestion system. 

Currently, in `/app/`, there is a multi-service backup ingestion pipeline consisting of:
1. **Nginx** (Reverse proxy, listening on port 8080)
2. **Flask API** (Python application handling the uploads, running on port 5000)
3. **Redis** (In-memory datastore, running on port 6379)

The Flask app accepts `.tar.gz` backup streams via a `POST /upload` endpoint and extracts them into `/home/user/backups/`.

However, the storage administrator has identified several critical issues that you must fix:
1. **Nginx Upload Limit:** Nginx is currently rejecting large backup files. You must reconfigure `/app/nginx/nginx.conf` to allow client requests up to 500MB.
2. **Security Vulnerability (Path Traversal):** The current Python implementation naively extracts tar files. A malicious backup containing files with paths like `../../home/user/pwned.txt` or absolute paths like `/etc/hacked` will overwrite files outside the target directory. You must modify `/app/api/app.py` to sanitize incoming paths. Any file attempting to escape the extraction directory must have its path normalized so it is safely extracted *inside* `/home/user/backups/<backup_id>/`.
3. **Storage Inefficiency:** Backups contain many identical files (e.g., unchanged application binaries across daily backups). You must implement an inline deduplication mechanism in `/app/api/app.py`. As you extract files from the compressed stream, compute the SHA-256 hash of each file's contents. Use Redis to map these hashes to their first known file path. If a subsequent file has the same hash, do not write a new file; instead, create a hard link to the existing file on the filesystem to save disk space.

**Workflow Instructions:**
- The source code and configurations are located in `/app/`.
- Review `/app/nginx/nginx.conf`, `/app/redis/redis.conf`, and `/app/api/app.py`.
- Apply your fixes using Python and text manipulation.
- Start the services by running `/app/start.sh`.
- The verifier will send a series of large, highly-duplicated `.tar.gz` files (some containing malicious path traversals) to `http://localhost:8080/upload`.

**Success Criteria:**
1. All services must be running and successfully process the uploads.
2. Path traversal attempts must be neutralized (extracted safely inside the designated backup folder).
3. The deduplication implementation must achieve a **Deduplication Ratio (Logical Size / Physical Size) of >= 3.0** on the verifier's test dataset. 

Do not write any test scripts yourself. Just implement the system, start it, and exit.