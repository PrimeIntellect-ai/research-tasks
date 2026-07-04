You are a log analyst investigating anomalous access patterns. We have a local logging pipeline that is currently broken. Your goal is to repair the log ingestion pipeline (Nginx -> Vector -> Redis) and write a highly optimized Python data processing tool to analyze the logs.

### Part 1: Repair the Multi-Service Pipeline
There are three services configured to run in user-space:
1. Nginx (listening on port 8080)
2. Vector (log router)
3. Redis (listening on 127.0.0.1:6379)

Currently, Nginx and Vector are not configured correctly.
1. **Nginx**: Modify the Nginx configuration at `/home/user/services/nginx/nginx.conf`. 
   - Define a new log format named `json_log`. It must be a valid JSON object with exact keys: `timestamp` (using `$msec`), `user_id` (using `$http_x_user_id`), `endpoint` (using `$uri`), and `latency` (using `$request_time`).
   - Configure the server block to write access logs to `/home/user/services/logs/access.log` using this `json_log` format.
2. **Vector**: Modify the Vector configuration at `/home/user/services/vector/vector.toml`.
   - Set up a source to tail the `/home/user/services/logs/access.log` file.
   - Parse the incoming lines as JSON.
   - Set up a Redis sink that pushes the parsed JSON to the Redis server at `127.0.0.1:6379` into a list key named `live_access_logs`.

You can restart the services using the provided script: `/home/user/manage_services.sh restart`

### Part 2: Data Processor Script
Write a Python script at `/home/user/log_transform.py` to analyze extracted log files. 
The script must take a single command-line argument: the path to a JSONL file containing log records (same format as the `json_log`).

Your script must perform the following operations:
1. **Multi-format I/O**: Read the input JSONL file.
2. **Parallel Processing**: Group the data by `user_id` and process each user's data in parallel using Python's `multiprocessing` module (or `concurrent.futures`).
3. **Sorting**: For each user, sort their events strictly by `timestamp` (ascending).
4. **Windowed Aggregation**: Calculate a rolling 3-event simple moving average (SMA) of the `latency`. For the first event, the SMA is just its latency. For the second, it's the average of the first two. From the third onwards, it's the average of the current and two previous latencies.
5. **Distance Computation**: Calculate the absolute difference (1D Euclidean distance) between the current event's `latency` and the immediately preceding event's `latency`. For the first event, this distance is `0.0000`.
6. **Output**: Combine all processed user records, sort the global dataset first by `timestamp` (ascending), then by `user_id` (alphabetically). Print the result to `stdout` as a strict CSV (comma-separated, no spaces) with a header row:
   `timestamp,user_id,endpoint,latency,rolling_avg_latency,latency_diff`
   
**Formatting Rules**:
- `timestamp`: String (exactly as read).
- `latency`, `rolling_avg_latency`, `latency_diff`: Floats formatted to exactly 4 decimal places (e.g., `0.1200`).

Your script must produce output that perfectly matches our strict internal reference implementation for arbitrary test logs.