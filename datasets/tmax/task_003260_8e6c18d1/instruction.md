You are tasked with building a Configuration Manager Tracking Service that acts as a real-time bridge between a legacy proprietary archive system and a modern HTTP API.

Our system receives configuration updates as proprietary `.cpk` (ConfigPack) archive files in the `/home/user/spool/` directory. 
We have provided a legacy tool, located at `/app/cpk_tool` (a stripped binary). This tool reads a `.cpk` archive from standard input, verifies its integrity, decompresses the payload, and outputs the plain-text configuration to standard output. If the archive is corrupt or invalid, it exits with a non-zero status.

Unfortunately, `/app/cpk_tool` discards the crucial timestamp metadata embedded in the `.cpk` header. By analyzing `.cpk` files or reverse-engineering the binary, you'll find that the files begin with a specific magic sequence, followed immediately by a 32-bit Little-Endian unsigned integer representing the Unix timestamp.

Your objective is to write a background service (in Python, Node.js, Ruby, or another language of your choice) that implements the following multi-stage workflow:

1. **Watch and Lock:** Watch the `/home/user/spool/` directory for new `.cpk` files. Ensure you handle file locking or concurrent access properly so that files are not read while they are still being actively written to the directory.
2. **Header Extraction:** For every valid `.cpk` file, parse the binary header natively in your code to extract the 32-bit Little-Endian Unix timestamp (located at byte offset 4).
3. **Archive Integrity and Redirection:** Pipe the file contents to `/app/cpk_tool` to verify its integrity and extract the decompressed configuration payload. Handle standard streams and exit codes appropriately.
4. **Multi-Protocol API Server:** Expose an HTTP server listening exactly on `127.0.0.1:8181`. 
   - All requests must require the following header: `Authorization: Bearer conf-sync-secret`
   - Implement `GET /latest`: This endpoint must return a JSON response containing the extracted timestamp and payload from the *most recently timestamped* valid `.cpk` file in the spool directory.
     Format: `{"status": "ok", "timestamp": <integer>, "data": "<decompressed_string>"}`
   - Implement `POST /upload`: This endpoint must accept a raw binary payload in the request body and safely write it to a new file in `/home/user/spool/` (using a safe naming scheme and ensuring the watcher doesn't read it prematurely). Return `{"status": "saved"}`.

Please implement the solution, start your service in the background, and create a log file at `/home/user/service_ready.log` containing the text "SERVICE RUNNING" once your API is bound and ready to accept requests.