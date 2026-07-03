You are a DevOps engineer tasked with debugging a critical log processing pipeline. Our system ingests binary log fragments (represented as hex strings) via a web API, queues them, and processes them to compute service metrics. However, the pipeline is currently broken in multiple ways: services are misconfigured, and the data processing logic suffers from integer overflow issues reminiscent of a 32-bit signed vs unsigned mismatch.

The system is located in `/app/` and consists of:
1. **Redis**: Running on `localhost:6379` (started automatically).
2. **Flask Ingress API** (`/app/api.py`): Supposed to listen on port 5000, receive `POST /ingest` requests with a JSON payload `{"log": "<16-char-hex>"}`, and push the hex string to a Redis list named `log_queue`.
3. **Log Worker** (`/app/worker.py`): Polls `log_queue` from Redis, parses the hex string using `/app/log_parser.py`, and writes the resulting JSON to `/app/processed_logs.json`.
4. **Log Parser** (`/app/log_parser.py`): A utility script that parses the 16-character hex string.

**Your objectives:**

1. **Fix the Environment/Configuration:**
   The Flask API and Log Worker are failing to communicate with Redis and each other. Identify and fix the connection string/port configurations in `/app/api.py` and `/app/worker.py`. 

2. **Fix the Parsing Edge-Case (Integer Overflow):**
   The 16-character hex string represents two 32-bit integers in Little Endian format. 
   - The first 8 characters (4 bytes) represent `event_id`.
   - The last 8 characters (4 bytes) represent `duration_ms`.
   Currently, `/app/log_parser.py` misinterprets large `duration_ms` values as negative numbers due to incorrect unpacking (e.g., treating it as a signed integer), which breaks our downstream metrics formulas.
   Modify `/app/log_parser.py` to correctly parse these values as **unsigned 32-bit integers**.
   
   The parser must be runnable from the CLI. When executed as `python3 /app/log_parser.py <16-char-hex>`, it must print a single valid JSON object to `stdout` with the keys `"event_id"` and `"duration_ms"`.

To ensure your parser is 100% correct, we have provided a reference binary at `/app/oracle_parser`. Your fixed `python3 /app/log_parser.py <hex_string>` must produce bit-exact equivalent output to `/app/oracle_parser <hex_string>` for ANY valid 16-character hex string. 

Leave the final, fixed version of `/app/log_parser.py` and the fixed service files in their original locations in `/app/`.