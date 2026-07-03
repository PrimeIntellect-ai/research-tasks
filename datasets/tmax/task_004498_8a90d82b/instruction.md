You are a storage administrator managing a custom archival system. Users upload custom chunked archives ("CHNK" format) via a web service. Recently, we have experienced disk fill-ups and Out-Of-Memory (OOM) crashes due to maliciously crafted or corrupted archives. 

Your task is to create a fast, resilient C++ filter program to classify these archives, and integrate it into our multi-service ingestion pipeline.

**System Architecture:**
- **Nginx** (listening on port 8080) acts as a reverse proxy.
- **Flask Python App** (listening on port 5000) handles the upload logic.
- **Redis** (listening on port 6379) tracks upload statistics.
These services are already running in the background.

**Task Requirements:**

1. **Write a C++ Filter:**
   Create a C++ program and compile it to `/home/user/archive_filter`. The program must take a single command-line argument: the absolute path to a CHNK archive file.

   The CHNK binary format is strictly defined as:
   - **Magic Header:** 4 bytes, must be exactly the ASCII characters `CHNK`.
   - **Chunk Count:** 4-byte unsigned integer (little-endian) representing the number of chunks.
   - **Chunks:** For each chunk sequentially:
     - **Size:** 4-byte unsigned integer (little-endian) representing the size of the chunk data in bytes.
     - **Data:** `Size` bytes of raw payload.

   Your program must parse the file and determine if it is "clean" or "evil". 
   It must exit with code `0` if the file is cleanly formatted, or exit with code `1` if it is evil.
   
   An archive is considered **evil/invalid** if ANY of the following are true:
   - The magic header is missing or incorrect.
   - Any individual chunk specifies a size strictly greater than `1048576` bytes (1 MB).
   - The file is truncated (ends before all specified chunks and their data can be fully read).
   - There are trailing garbage bytes after all chunks have been parsed (the file size does not perfectly match the header + sum of chunk sizes).

2. **Integrate with the Ingestion Pipeline:**
   The Flask app reads its configuration from `/app/flask_app/config.ini`. 
   Currently, the filter command is not set. You must edit `/app/flask_app/config.ini` and set the `FILTER_CMD` key under the `[Upload]` section to the absolute path of your compiled binary:
   `FILTER_CMD=/home/user/archive_filter`
   (The Flask app dynamically reloads this configuration on every request, so you do not need to restart the service).

**Testing Your Filter:**
To help you develop, we have provided two sets of sample archives:
- `/home/user/corpus/clean/` contains valid archives. Your program MUST exit `0` for all of these.
- `/home/user/corpus/evil/` contains malformed or malicious archives. Your program MUST exit `1` for all of these.

You must ensure your `/home/user/archive_filter` binary is compiled, executable, and strictly adheres to the return code specifications, as the automated verifier will both test it directly against a hidden adversarial corpus and test the end-to-end Nginx/Flask pipeline.