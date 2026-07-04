You are a log analyst investigating anomalous patterns and malicious payload injections in a highly concurrent distributed system. Our raw logging pipeline currently receives events in a "wide" JSON format, but we are seeing corrupted entries and injection attempts. 

Your task is to build a high-performance log sanitizer in Rust and integrate it into our multi-service pipeline.

Step 1: The Rust Sanitizer
Create a Rust project in `/home/user/log_sanitizer`. The application must compile to a CLI tool that accepts the following arguments:
`cargo run --release -- --input <input_path> --output <output_path>`

The application must read a JSON Lines (JSONL) file from `<input_path>` (where each line is a wide JSON object with varied, unpredictable keys), process the lines in **parallel** (e.g., using the `rayon` crate), and write the surviving valid logs to `<output_path>` in the exact same JSON format.

Validation Rules:
To validate the logs, your Rust program must conceptually or literally reshape the wide JSON into a long format (key-value pairs) to apply the following constraint-based validations to *every* field:
1. **String Constraints:** No string value in the entire JSON object (at any depth) may contain the case-insensitive substrings `"<script>"` or `"DROP TABLE"`. If found, drop the entire log line.
2. **Numeric Constraints:** If a field named `status_code` exists, it must be an integer between 100 and 599 inclusive. If it falls outside this range, drop the log line.
3. **Format Constraints:** If a field named `timestamp` exists, it must strictly follow the ISO-8601 format (e.g., `2023-10-12T07:20:50.52Z`). If malformed, drop the log line.

Step 2: Adversarial Corpus Testing
Your sanitizer must be perfectly accurate. We have provided two datasets for you to test against:
- `/app/corpus/clean/`: Contains `clean_logs.jsonl`. Your program must preserve 100% of these lines.
- `/app/corpus/evil/`: Contains `evil_logs.jsonl`. Your program must reject 100% of these lines (the output file should be empty).

Step 3: Multi-Service Integration
In `/app/services/`, there are two cooperating services:
- `producer.py`: A simulated upstream service that continuously writes raw JSONL logs to a named pipe at `/tmp/raw_logs.fifo`.
- `consumer.py`: A downstream log indexer that expects sanitized JSONL logs on a named pipe at `/tmp/clean_logs.fifo`.

A startup script `/app/services/start_pipeline.sh` creates the FIFOs and starts both Python services in the background. 
You must write a bash wrapper `/home/user/run_bridge.sh` that executes your Rust binary, connecting it continuously to the running pipeline (reading from `/tmp/raw_logs.fifo` and writing to `/tmp/clean_logs.fifo`). Ensure your Rust program can handle streaming input from a FIFO without buffering indefinitely.

Output Requirements:
- The compiled binary must exist at `/home/user/log_sanitizer/target/release/log_sanitizer`.
- Leave the wrapper script at `/home/user/run_bridge.sh` and ensure it is executable.