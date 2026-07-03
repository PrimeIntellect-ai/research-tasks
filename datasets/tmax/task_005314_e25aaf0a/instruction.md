Hello! I am a researcher organizing a massive amount of sensor data, and I need your help setting up a data ingestion and serving pipeline. 

I have a dataset archive located at `/app/dataset.tar.gz`. This archive contains nested `.zip` files, each corresponding to a specific sensor (e.g., `sensor_alpha.zip`, `sensor_beta.zip`). Inside each zip file, there are two files:
- `meta.txt`: A plain text file containing sensor metadata.
- `data.bin`: A large binary file containing the raw readings.

I need you to build a system that unpacks, processes, and serves this data using Go, Redis, and Nginx. 

Here are your exact requirements:

1. **Archive Handling & File Processing (Go)**
   Write a Go program at `/home/user/server.go` that:
   - Safely unpacks the dataset and its nested zip files.
   - For each sensor, reads the `data.bin` file and splits it into chunks of exactly 1,000,000 bytes (the final chunk may be smaller).
   - Uses atomic writes (via temp files and renaming) to save these chunks into `/home/user/processed/<sensor_name>/chunk_<index>.bin` (0-indexed).
   - Reads the `meta.txt` file for each sensor.

2. **Metadata Storage**
   - Connect to the local Redis instance running on `127.0.0.1:6379` (no password).
   - For each sensor, store the total number of chunks generated as a string under the key `sensor_chunks:<sensor_name>`.

3. **HTTP API (Go)**
   - The Go program must start an HTTP server listening on `127.0.0.1:8080`.
   - Expose `GET /api/data/{sensor_name}/meta` which returns the exact text from that sensor's `meta.txt`.
   - Expose `GET /api/data/{sensor_name}/chunk/{index}` which returns the binary data for the requested chunk index.

4. **Service Composition & Gateway**
   - We are using an existing Nginx instance to act as our API gateway. The configuration file is located at `/app/nginx.conf`.
   - Modify `/app/nginx.conf` so that any request to `/api/` on port `8090` is reverse-proxied to your Go service at `http://127.0.0.1:8080`.
   - A script at `/app/start_services.sh` is provided. Run this script once you have modified the Nginx config. It will start Redis on port 6379 and Nginx on port 8090 in the background.
   - You must run your Go server in the background so it is actively serving requests when you complete the task.

Ensure all services are running and appropriately linked. I will test the pipeline by querying the gateway on port 8090.