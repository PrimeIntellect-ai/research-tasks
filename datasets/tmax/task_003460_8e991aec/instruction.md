You are an engineer tasked with building a time-series configuration change tracker. We receive thousands of configuration change events globally across different microservices. Some misconfigured automated systems are applying changes too rapidly, causing race conditions. 

Your objective is to build a multi-stage data processing pipeline using Rust that streams these configuration events, sorts them, and enforces a temporal validation gate to identify rate-limit violations.

**The Input:**
A large JSONL file located at `/home/user/config_events.jsonl`.
Each line contains a single JSON object representing a configuration change event:
```json
{"timestamp": 1698765432000, "service": "認証サービス", "change_id": "uuid-1234", "payload_size": 256}
```
*   `timestamp`: Epoch time in milliseconds.
*   `service`: The name of the service (contains multi-language Unicode characters).
*   `change_id`: Unique identifier for the change.
*   `payload_size`: Size of the config payload.

**Your Task:**
1. Initialize a Rust project at `/home/user/config_tracker`. You may use popular crates like `serde`, `serde_json`, and `csv`.
2. Write a Rust program that streams `/home/user/config_events.jsonl` efficiently (do not load the entire file into memory at once, as the real file can be larger than RAM).
3. Group the events by the `service` field.
4. For each service, sort the events chronologically by `timestamp` (ascending).
5. Apply a **Validation Quality Gate**: Iterate through the sorted events for each service. If a change occurs strictly less than `1000` milliseconds after the *immediately preceding* change for that *same* service, it is considered a violation.
6. Output the violations to a CSV file located at `/home/user/invalid_changes.csv`.

**Output Format Constraints (`/home/user/invalid_changes.csv`):**
*   The CSV must have the exact header: `service,timestamp,change_id`
*   The rows must only contain the events that violated the 1000ms rule (the second event in the rapid succession).
*   The rows must be sorted primarily by `service` name (alphabetical Unicode scalar value order, ascending), and secondarily by `timestamp` (ascending).
*   Example row: `認証サービス,1698765432500,uuid-5678`

Write the Rust code, compile it, and run it to produce the final `invalid_changes.csv`.