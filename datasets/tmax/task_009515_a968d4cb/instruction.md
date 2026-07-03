You are acting as a log analyst investigating a potential coordinated attack on our distributed systems. You have been provided with two large log files in different formats. 

Your task is to write a Rust application that processes these log streams, performs constraint-based validation, correlates suspicious activities across the two sources, and logs its own pipeline execution.

The log files are located at:
1. `/home/user/logs/auth.csv`: A CSV file with headers `timestamp,ip_address,status,username`.
2. `/home/user/logs/app.jsonl`: A JSON Lines file where each line is a JSON object with keys `{"ts": "...", "level": "...", "msg": "..."}`.

Follow these requirements to build the pipeline:

1. **Environment Setup**: Initialize a new Rust binary project at `/home/user/log_analyzer`. You may use standard crates like `serde`, `serde_json`, `csv`, and `regex`.

2. **Pipeline Logging**: Your program must log its execution progress. It should append the following exact messages (one per line) to `/home/user/pipeline.log` at the appropriate times:
   - `[INFO] Pipeline started`
   - `[INFO] Processing auth.csv`
   - `[INFO] Processing app.jsonl`
   - `[INFO] Pipeline finished`

3. **Processing `auth.csv`**:
   - Stream the file efficiently (do not load the entire file into memory at once).
   - Validate that the `ip_address` field is a strictly valid IPv4 address. Discard rows with invalid IPs.
   - Find all valid IP addresses that have **strictly more than 3** log entries where `status` is exactly `FAILED`.

4. **Processing `app.jsonl`**:
   - Stream the file line-by-line.
   - Filter for lines where the `level` is exactly `"ERROR"`.
   - For these error lines, parse the `msg` field and extract any valid IPv4 address found within the text.

5. **Correlation and Output**:
   - Find the intersection of the IPs: IPs that both failed authentication >3 times AND appeared in at least one `ERROR` message in the application logs.
   - Write this final list of highly suspicious IP addresses to `/home/user/flagged_ips.json`. The file must contain a single JSON array of strings, sorted alphabetically (e.g., `["10.0.0.1", "192.168.1.5"]`).

Once you have written the code, compile it using `cargo build --release` and run the executable to produce the output files.