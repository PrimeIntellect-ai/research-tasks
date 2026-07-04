You are an infrastructure developer tasked with organizing and archiving legacy project files for a distributed internal system. The system relies on three microservices that must be properly glued together. 

First, initialize the local services by running:
`bash /app/start_services.sh`
This brings up:
1. An Nginx server serving raw project files on `127.0.0.1:8080`.
2. A Redis server caching file metadata on `127.0.0.1:6379`.
3. A Flask coordinator API on `127.0.0.1:5000`.

**Step 1: Service Reconfiguration**
The Flask app is currently failing because it's misconfigured. 
Edit `/app/coordinator/config.json` so that:
- `redis_host` is set to `"127.0.0.1"` (instead of the default socket path)
- `redis_port` is set to `6379`
- `storage_url` is set to `"http://127.0.0.1:8080/files/"`
Restart the Flask app by killing the existing python process and running `python3 /app/coordinator/app.py &`.

**Step 2: Archive Generation (C++)**
Write a C++ program at `/home/user/archiver.cpp` that performs the following workflow:
1. Fetch the list of file IDs to archive by making an HTTP GET request to `http://127.0.0.1:5000/api/stale_ids`. (This returns a comma-separated list of IDs).
2. For each ID, query the local Redis server for the key `file:<ID>`. The value is a JSON string containing file metadata. Extract the `"filepath"` and `"is_text"` boolean.
3. Download the actual file content from Nginx using the URL: `<storage_url><filepath>`.
4. **Custom Pre-processing:** To save maximum space, for any file where `"is_text": true`, strip all carriage returns (`\r`) and replace any sequence of two or more spaces with a single space BEFORE archiving. 
5. Concatenate all processed file buffers and compress the combined stream using standard `zlib` (gzip format).
6. Write the final gzipped archive to `/home/user/stale_archive.gz`.

Compile your C++ program (you may use `libcurl`, `hiredis`, `nlohmann-json3-dev`, and `zlib1g-dev` which are installed) and run it to produce the archive.

**Evaluation:**
Your final output will be graded by an automated verifier that measures the file size of `/home/user/stale_archive.gz`. To pass, your archive must correctly contain all stale files, properly pre-processed, and achieve a highly optimized file size under a specific byte threshold.