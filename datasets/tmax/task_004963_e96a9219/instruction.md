You are a storage administrator managing disk space and archiving on a Linux system. You need to automate a workflow that processes log files for a specific storage zone, archives them, and serves an API to manage an index of the files.

Follow these steps carefully:

1. **Identify the Target Zone**: 
   There is an image file at `/app/system_tag.png`. Use OCR (e.g., `tesseract`) to extract the text from this image. The extracted text (ignoring leading/trailing whitespace) is the "Zone ID".

2. **Bulk File Renaming**:
   Look in the directory `/app/logs/`. You will find several files named with the pattern `raw_<ZoneID>_<number>.log`. 
   Rename all files that match the extracted Zone ID to `processed_<ZoneID>_<number>.log`. Leave files belonging to other zones untouched.

3. **Archiving**:
   Create a compressed tarball (`.tar.gz`) containing all the newly renamed `processed_<ZoneID>_*.log` files. The archive must be saved exactly at `/app/archive_<ZoneID>.tar.gz` and should not contain absolute paths (the files should be at the root of the archive or under a `logs/` directory relative to the archive root).

4. **Web Service with Concurrency Control**:
   Write and start a Python HTTP server listening on `127.0.0.1:8888`. The server must run continuously.
   The server must implement the following endpoints:
   
   - `GET /info`: 
     Returns a JSON response `{"zone": "<Zone ID>", "files_archived": <N>}`, where `<N>` is the integer number of files you renamed and archived.
     
   - `POST /register`: 
     Accepts a JSON payload like `{"filename": "some_file.log"}`.
     The server must maintain a JSON array in `/app/registry.json` (initialize it as an empty array `[]` if it doesn't exist).
     Upon receiving this POST request, the server must append the new filename to the array.
     **Crucially**, because multiple clients may hit this endpoint concurrently, your server must safely update `/app/registry.json` using **file locking** (e.g., `fcntl.flock`) and **atomic writes** (write the updated JSON array to a temporary file, then perform an atomic rename/replace over `/app/registry.json`).

Ensure your Python server is running and bound to the correct port before you declare the task finished.