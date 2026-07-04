You are assisting a technical writer in overhauling a documentation processing pipeline. We have a Go-based processor that ingests documentation archives, but it has several critical issues: it is vulnerable to directory traversal (tar slip), it is incredibly slow, and our downstream services are disconnected.

Your objective is to fix the pipeline, optimize it, and glue the services together.

**System Overview:**
We have a multi-service stack located in `/app/services/`:
1. **Redis**: Runs on port 6379. Stores documentation revision timestamps.
2. **Flask API**: Runs on port 5000. Serves documentation metadata fetched from Redis.
3. **Nginx**: Front-end reverse proxy running on port 8080.

**Step 1: Fix Service Configuration**
- Start the services using `/app/services/start_all.sh`.
- Update the Nginx configuration at `/app/services/nginx.conf` so that any request to `http://127.0.0.1:8080/api/` is properly proxied to the Flask API at `http://127.0.0.1:5000/`. Reload Nginx once fixed.

**Step 2: Secure and Optimize the Go Processor**
You have been provided a reference Go script at `/home/user/process_docs.go`. This script processes documentation tarballs, but has two flaws:
1. **Tar Slip Vulnerability**: The archive `/app/data/docs_upload.tar` contains malicious paths (e.g., `../../etc/passwd` or `../outside.md`). The script currently extracts these blindly. Modify the Go code to *skip* any file in the archive that attempts to traverse outside the target extraction directory (`/tmp/docs_out/`).
2. **Performance**: The script processes files sequentially. Modify it to extract and process files concurrently using goroutines.

**Step 3: Implement Domain-Specific Parsing (WAL)**
The tarball contains a special binary file named `history.wal`. Modify your Go program so that, upon encountering this file in the archive, it parses it and updates Redis.
- **WAL Format**: Sequence of 9-byte records. 
  - Bytes 0-3: `uint32` Document ID (Little Endian)
  - Bytes 4-7: `uint32` Unix Timestamp (Little Endian)
  - Byte 8: `uint8` Status Flag
- **Action**: If the Status Flag is `1`, your Go program must write to Redis: key=`doc:{Document ID}`, value=`{Timestamp}`. You may use standard Go Redis libraries (e.g., `github.com/go-redis/redis/v8`) or just shell out to `redis-cli`.

**Verification:**
Once you have modified `/home/user/process_docs.go`, compile it to `/home/user/process_docs`. 
We will evaluate your compiled binary using `/app/verify.sh`. 
This script will check:
1. End-to-end API connectivity (Nginx -> Flask -> Redis).
2. Security: Ensure no files were extracted outside `/tmp/docs_out/`.
3. Accuracy: Redis must contain the correct parsed WAL data.
4. **Metric Threshold**: Your concurrent Go program must achieve a **speedup of >= 3.0x** compared to our reference binary `/app/bin/process_docs_ref` when processing the large dataset `/app/data/large_docs.tar`.