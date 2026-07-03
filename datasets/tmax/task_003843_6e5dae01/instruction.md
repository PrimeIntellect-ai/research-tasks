You are a backup administrator responsible for consolidating and serving archived data. 

We have a custom archiving tool shipped as a vendored Go package, but it is currently failing to build on our Linux infrastructure. You need to fix the archiving tool, generate an archive of our system's raw data, create a metadata index, and expose everything via a reliable HTTP service.

Your objectives:

1. **Fix the Archiver Tool:**
   Navigate to the vendored package at `/app/vendored/fast-tar`. This tool is used to package directories into our proprietary `.ftar` backup format. It currently fails to build correctly for our environment. Identify the issue (hint: check the build scripts/environment variables), fix it, and build the `fast-tar` executable.

2. **Index the Raw Data:**
   We have raw data (JSON, CSV, XML) stored in `/home/user/raw_data/`. 
   Write a Go script (or use bash/awk/sed) to iterate over all files in `/home/user/raw_data/` and compute their SHA256 hashes. 
   Save the output to `/home/user/index.json` strictly in this JSON format:
   ```json
   {
     "files": [
       {"path": "sales/Q1.csv", "hash": "<sha256>"},
       {"path": "users.xml", "hash": "<sha256>"}
     ]
   }
   ```
   (Paths must be relative to `/home/user/raw_data/`).

3. **Archive the Data:**
   Use the compiled `fast-tar` tool to archive the `/home/user/raw_data/` directory. Save the output archive to `/home/user/backup.ftar`. 
   (Usage: `./fast-tar -out /home/user/backup.ftar /home/user/raw_data/`)

4. **Serve the Backup:**
   Write a Go HTTP server and run it. The server must:
   - Listen on `0.0.0.0:9090`.
   - `GET /ping`: Return the exact text `pong`.
   - `GET /index`: Serve the `/home/user/index.json` file.
   - `GET /download`: Serve the `/home/user/backup.ftar` file with the header `Content-Type: application/octet-stream`.

Start the server in the background so it remains running.