You are tasked with optimizing a configuration manager's state tracking system. We have a multi-service setup (Nginx, Flask, Redis) that serves configuration history. Currently, the raw configuration changes are stored as thousands of verbose JSON files, which are too large and slow to load.

Your objectives:

1. **Format Conversion & Transformation**:
   In `/home/user/data/raw_configs`, there are 5,000 JSON files. Each file looks like:
   ```json
   {
     "timestamp": "1670000000",
     "service": "api_gateway",
     "config": {
       "rate_limit": 100,
       "timeout": 30
     }
   }
   ```
   Use standard CLI tools (like `jq`, `awk`, `sed`) to parse all these files and transform them into a single, sorted CSV file at `/home/user/data/configs.csv`. 
   The CSV format must strictly be: `timestamp,service,rate_limit,timeout`. Sort the lines chronologically by timestamp.

2. **Custom Compression (Python)**:
   Write a Python script `/home/user/scripts/compress.py` that reads `/home/user/data/configs.csv` and compresses it into a binary file `/home/user/data/configs.dat`. 
   To meet our strict storage requirements, your compression must achieve a file size of **less than 85,000 bytes**. You may use delta-encoding on the timestamps, run-length encoding on the service names, and Python's built-in `zlib` or `bz2` libraries to achieve this. 

3. **Service Configuration & Startup**:
   Our application stack is located in `/home/user/app/`. It consists of:
   - A Redis server (default port 6379)
   - A Flask application (runs on port 5000)
   - An Nginx reverse proxy (runs on port 8080)
   
   Configure Nginx by editing `/home/user/app/nginx.conf` so that all HTTP requests to port 8080 are proxied to the Flask app on `127.0.0.1:5000`.
   
   The Flask app expects the environment variable `COMPRESSED_DATA_PATH` to point to your `/home/user/data/configs.dat` file, and an environment variable `DECOMPRESS_SCRIPT` pointing to a Python script `/home/user/scripts/decompress.py` that you must write. The `decompress.py` script should read `/home/user/data/configs.dat` and print the original CSV content to standard output.
   
   Start the services using the provided `/home/user/app/start_services.sh`.

4. **Verification**:
   Once running, a request to `curl http://localhost:8080/history` should return the full, correctly decompressed CSV data served from Redis cache.

Ensure your compression achieves the required size threshold, and that your decompression accurately restores the exact CSV text.