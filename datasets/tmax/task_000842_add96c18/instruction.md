You are a data engineer tasked with overhauling an unreliable ETL pipeline that aggregates server telemetry. The current system is suffering from three major issues: it double-counts records due to upstream retries, it crashes when malicious or malformed payloads are ingested, and it lacks the ability to compute rolling statistics. 

Your objective is to build a robust data sanitization filter and a real-time ETL daemon that orchestrates data flow between an upstream emitter, a Redis state store, and a downstream metric sink.

**Environment Setup**
We have provided a multi-service orchestration script. 
1. Run `/app/start_services.sh` to initialize the environment.
2. This will start:
   - **Telemetry Emitter** on `http://127.0.0.1:8080`. Endpoint `GET /metrics` returns a JSON array of telemetry records. This service simulates retries (yielding duplicate `id`s) and occasionally outputs malformed/malicious records.
   - **Data Sink** on `http://127.0.0.1:9090`. Endpoint `POST /aggregate` accepts aggregated statistics.
   - **Redis** on `127.0.0.1:6379`.

**Requirement 1: Data Sanitizer (Adversarial Filter)**
Before processing data in the ETL, you must write a standalone robust sanitization CLI at `/home/user/sanitizer.py`. 
It must strictly enforce the following schema and constraints. Malformed JSON or records violating ANY of these rules must be silently dropped.
- `id`: Must be a valid UUIDv4 string.
- `timestamp`: Must be a valid ISO8601 formatted string.
- `host`: Must only contain alphanumeric characters and hyphens (regex: `^[a-zA-Z0-9\-]+$`). No spaces, quotes, or injection characters allowed.
- `cpu_usage`: Must be a numeric value (int or float) between `0.0` and `100.0` inclusive.

The CLI must accept an input JSONL file and write valid records to an output JSONL file:
`python3 /home/user/sanitizer.py <input.jsonl> <output.jsonl>`
*Note: An automated verification suite will test this script against a hidden corpus of clean and malicious files.*

**Requirement 2: Real-time ETL Daemon**
Write an orchestration script at `/home/user/etl_daemon.py` that continuously polls the Emitter (every 1 second) and processes the data:
1. **Sanitize:** Apply the exact same filtering rules defined in your sanitizer to the polled data.
2. **Deduplicate:** Use Redis to ensure each `id` is processed *exactly once*. The upstream emitter will retry batches, so you will see the same `id` multiple times. Deduplication keys should expire after 1 hour.
3. **Rolling Statistics:** For each valid, newly-seen record, compute the rolling 5-minute average of `cpu_usage` for its specific `host`. Use Redis (e.g., Sorted Sets) to maintain this rolling window based on the record's `timestamp`. 
4. **Load:** Immediately after updating a host's window, push the new aggregate to the Data Sink:
   `POST http://127.0.0.1:9090/aggregate`
   Payload format: `{"host": "<host_name>", "timestamp": "<latest_record_timestamp>", "avg_cpu_5m": <float_average>}`
5. **Log:** Write an execution log to `/home/user/pipeline.log` tracking the number of records polled, dropped, deduplicated, and successfully forwarded.

Leave the `etl_daemon.py` running in the background when you are finished. Create `/home/user/ready.flag` to signal completion.