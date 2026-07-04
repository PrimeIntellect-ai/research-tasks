You are acting as a log analyst investigating anomalous patterns in a microservices architecture. Our log ingestion pipeline is currently broken, and we also need a robust log parsing script to analyze the data.

Your goal has two parts: 
1. Fix the multi-service pipeline so logs flow correctly.
2. Implement a Python log analyzer that exactly matches the behavior of our legacy compiled binary, `/app/oracle_parser`.

**Part 1: Fix the Pipeline**
We have three services managed by `/app/start_services.sh`:
- A **Redis** message broker (runs on port 6379).
- A **Log Generator** (simulates service logs) that should push raw logs to Redis.
- A **Flask API** that reads from Redis and serves the logs via an HTTP endpoint.

Currently, the logs are not reaching the Flask API. 
- The Log Generator configuration is in `/home/user/generator_config.env`.
- The Flask API configuration is in `/home/user/flask_config.env`.
Investigate these configurations, fix the ports and Redis keys so that the Log Generator pushes to the `incoming_logs` list on Redis port 6379, and the Flask API reads from the exact same list. Once fixed, restart the services. You can verify it works if `curl http://localhost:5000/logs` returns a list of recent logs instead of an empty array.

**Part 2: Build the Log Analyzer**
We need to replace our legacy parser `/app/oracle_parser` with a Python script located at `/home/user/log_analyzer.py`.
Your script must process text lines from `STDIN` and output exactly matching lines to `STDOUT`. Our automated verifier will blast thousands of generated logs into both your script and the oracle; your script's output must be bit-exact identical to the oracle.

Here are the processing rules you must implement:
1. **Input Format**: Comma-separated values: `timestamp,level,service,message`. (Assume valid CSV, no embedded commas in fields).
2. **Filtering**: Completely ignore and drop any lines where `level` is exactly `TRACE` or `DEBUG`.
3. **Deduplication**: Calculate the SHA256 hex digest of the string formed by concatenating `service` and `message` (i.e., `service + message`). If you have already output a line with this hash during the current execution, drop the new line.
4. **Alerting**: Determine an `alert` boolean. It should be `true` if `level` is `ERROR` or `FATAL`, and `false` otherwise.
5. **Output Format**: For each accepted line, output a strict JSON string on a single line. The JSON keys must be sorted alphabetically, and you must use compact separators (no spaces after commas or colons).
   The JSON object must contain exactly these keys:
   - `alert`: (boolean)
   - `hash`: (string, the SHA256 hex digest)
   - `service`: (string)
   - `timestamp`: (string)

Ensure your Python script has executable permissions (`chmod +x /home/user/log_analyzer.py`) and includes a proper shebang (`#!/usr/bin/env python3`).