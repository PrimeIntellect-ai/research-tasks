You are tasked with fixing a broken configuration deployment pipeline and implementing a custom archive tool for our configuration manager. 

Part 1: Service Integration
We have a local staging environment that uses three services to manage deployment metadata:
1. An Nginx reverse proxy (listening on port 8080).
2. A Flask API service.
3. A Redis instance.

Currently, the services are not communicating correctly. You need to fix their configurations so that:
- Nginx correctly routes requests from `http://127.0.0.1:8080/api/` to the Flask app.
- The Flask app (located in `/app/flask_service/app.py`) correctly connects to Redis. 
The startup script `/app/start_services.sh` is provided. You must modify the necessary configuration files in `/app/nginx/nginx.conf` and `/app/flask_service/config.env` so that a GET request to `http://127.0.0.1:8080/api/health` returns `{"status": "ok", "redis": "connected"}`. Ensure all services are restarted and running.

Part 2: The Configuration Archiver
We need a custom Python script, `/home/user/archiver.py`, that packages configuration files into a custom binary format. 
We have had issues in the past with backup scripts following cyclical symlinks into infinite loops, so your script must be robust against this.

Requirements for `/home/user/archiver.py`:
- It must accept a single command-line argument: the path to a target directory.
- It must recursively walk the target directory and follow symlinks. 
- **Cycle Prevention:** To prevent infinite loops, it must track the absolute, resolved path (using `os.path.realpath`) of directories it visits and skip any directory that has already been visited in the current traversal path.
- **File Filtering:** It must only process files with the `.conf` or `.yaml` extension.
- **Sorting:** To ensure deterministic output, the files must be processed in strictly alphabetical order based on their relative path to the target directory.

**Output Format (Written to standard output):**
1. A magic header: `CFG_BKP\x00` (8 bytes).
2. For each included file:
   - 16-bit unsigned integer (little-endian): The length of the relative file path.
   - The relative file path as a UTF-8 encoded string.
   - 32-bit unsigned integer (little-endian): The original, uncompressed size of the file in bytes.
   - 32-bit unsigned integer (little-endian): The compressed size of the file in bytes.
   - The payload: The file's contents, compressed using `zlib.compress()`.

Your script must be exact in its byte output, as it will be rigorously tested against a reference implementation using randomly generated directory structures with complex symlink graphs.