I am a researcher dealing with a large volume of historical and live sensor data, and I need a C-based system to organize, process, and serve this data efficiently. 

Here is my environment and what you need to do:
I have a multi-service setup in `/app/` that is currently misconfigured. It consists of Redis (intended for live data queuing), Nginx (for serving processed results), and a missing C-based processing daemon that you need to write.

**1. Historical Data Archiving (File I/O, Parsing, Archiving):**
In `/home/user/legacy_data/`, there is a deeply nested directory structure containing CSV files with sensor readings (format: `timestamp,sensor_id,value`). 
Write a C program (or add a module to your daemon) that recursively traverses this directory. For every `.csv` file found, use memory-mapped I/O (`mmap`) to read the file. Convert the data to a single unified JSON array of objects.
Once all CSVs are parsed and merged into this JSON structure, write the result to `/home/user/www/historical.json` and then create a compressed tarball of this JSON file at `/home/user/www/historical.tar.gz`.

**2. Live Data Processor (Multi-protocol, Services):**
Your C program must run as a daemon listening on TCP port `9000` (localhost).
- It must accept connections and require an initial authentication line: `AUTH sensor_token_99X`.
- Subsequent lines will be live JSON payloads (e.g., `{"timestamp": 1690000000, "sensor_id": 5, "value": 42.5}`).
- The daemon should parse these JSON payloads, calculate the running average of `value` per `sensor_id`, and push the latest averages to Redis (running on `127.0.0.1:6379`) in a Hash key called `sensor_averages`.
- It must also periodically (or synchronously) write these averages to a file at `/home/user/www/live_averages.json`.

**3. Glue & Configuration (Service Composition):**
Configure and start the provided Nginx server (using a local configuration in `/home/user/nginx.conf` and running as the `user`) to listen on `127.0.0.1:8080`.
Nginx must serve the static files from `/home/user/www/`:
- `GET /historical.tar.gz` should return the archive.
- `GET /live_averages.json` should return the live data averages.
Ensure Redis is running and accessible on its default port.

Use standard C libraries, POSIX APIs, `libjansson` (or `cJSON`), `libtar`/`zlib`, and `hiredis` as needed. You may use shell commands to install dependencies, start Redis/Nginx, and compile your C program. Please compile your program to `/home/user/sensor_daemon` and leave it running in the background.