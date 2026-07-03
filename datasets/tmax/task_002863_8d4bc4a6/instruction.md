You are a localization engineer managing a real-time translation telemetry pipeline. The system tracks the productivity and text expansion ratios of human translators in real-time. 

Currently, the telemetry pipeline is broken. You need to repair the multi-service architecture and implement a robust data processing filter in Python that handles resampling, gap-filling, and changepoint (anomaly) detection on a continuous stream of localization event logs.

### System Architecture (Multi-Service Compose)
The system consists of three components that must run concurrently:
1. **Redis**: Acts as the message broker. Must run on the default port `6379`.
2. **Emitter (`/app/emitter.py`)**: Simulates continuous translation logs. It pushes raw JSON telemetry logs to a Redis LIST named `loc_raw_stream`.
3. **Dashboard (`/app/dashboard.js`)**: A Node.js web dashboard (listens on port `8080`) that continuously pops processed logs from a Redis LIST named `loc_processed_stream` and displays them.

You must create a shell script at `/home/user/start_pipeline.sh` that starts all these services in the background and correctly connects them. 

### The Filter (`/home/user/loc_filter.py`)
To connect the raw stream to the processed stream, you must write a Python stream processor at `/home/user/loc_filter.py`. 
To ensure this filter is highly testable and language-agnostic, it must **read from standard input (`stdin`) and write to standard output (`stdout`)** line-by-line. Your `start_pipeline.sh` script should use a mechanism (like a small wrapper, `redis-cli`, or an inline python snippet) to pipe data from the `loc_raw_stream` Redis list, through your `loc_filter.py` via `stdin`/`stdout`, and push the output into the `loc_processed_stream` Redis list.

#### Filter Logic Rules (Bit-Exact Specification)
The input will be a stream of JSON lines. Each line is an object: `{"timestamp": 1620000000.0, "source_len": 45, "target_len": 52, "lang": "fr"}`.
You must process these line-by-line and print a JSON object to `stdout` for each event, applying the following rules:

1. **Streaming**: Read continuously. Do not buffer the entire file into memory.
2. **Gap-Filling**: The timestamp is a float (seconds). If the difference between the *current* event's timestamp and the *previous* actual event's timestamp is strictly greater than `2.0` seconds, you must insert synthetic "gap" events.
   - Insert a gap event every `1.0` second starting from `prev_timestamp + 1.0` until the synthetic timestamp is strictly less than the current timestamp.
   - Gap events must have the format: `{"timestamp": <syn_time>, "source_len": 0, "target_len": 0, "lang": "<prev_lang>", "anomaly": false, "is_gap": true}`.
   - Round synthetic timestamps to exactly 1 decimal place.
3. **Anomaly / Changepoint Detection**: For each *actual* event (not gap events), you must determine if the translation expansion ratio (`target_len / source_len`) is an anomaly.
   - Maintain a sliding window of the exact ratios of the last 5 *actual* events (do not include the current event in the window used to evaluate the current event).
   - If the window has fewer than 5 elements, `"anomaly": false`.
   - If the current event's `source_len` is 0, `"anomaly": false`.
   - Otherwise, if the current ratio is strictly greater than `2.0 * (sum_of_window / 5.0)`, set `"anomaly": true`. Else `"anomaly": false`.
4. **Actual Event Output Format**: Output the actual event with the newly added `"anomaly"` and `"is_gap"` fields (which will be `false` for actual events).

Example input:
```json
{"timestamp": 10.0, "source_len": 10, "target_len": 12, "lang": "de"}
{"timestamp": 13.5, "source_len": 10, "target_len": 15, "lang": "de"}
```
Example output:
```json
{"timestamp": 10.0, "source_len": 10, "target_len": 12, "lang": "de", "anomaly": false, "is_gap": false}
{"timestamp": 11.0, "source_len": 0, "target_len": 0, "lang": "de", "anomaly": false, "is_gap": true}
{"timestamp": 12.0, "source_len": 0, "target_len": 0, "lang": "de", "anomaly": false, "is_gap": true}
{"timestamp": 13.0, "source_len": 0, "target_len": 0, "lang": "de", "anomaly": false, "is_gap": true}
{"timestamp": 13.5, "source_len": 10, "target_len": 15, "lang": "de", "anomaly": false, "is_gap": false}
```

Ensure your `loc_filter.py` works perfectly as an independent UNIX filter. It will be verified by automated fuzzing against an oracle implementation.