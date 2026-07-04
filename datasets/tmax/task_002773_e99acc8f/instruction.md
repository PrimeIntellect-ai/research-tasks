You are a log analyst investigating patterns in a high-performance mathematical computation cluster. You need to build a robust shell-based ETL pipeline to process, clean, and schedule the ingestion of JSON/YAML log files.

However, the environment requires a specific tool that is currently broken.

Part 1: Environment Setup
We rely on the `yq` package (version 3.2.3) to normalize mixed YAML/JSON logs. The source code for this package is pre-vendored at `/app/yq-3.2.3`. Unfortunately, a previous developer made an incomplete modification to its `setup.py`, breaking the installation.
1. Fix the perturbation in `/app/yq-3.2.3/setup.py`.
2. Install the package locally for the user (e.g., `pip install --user -e /app/yq-3.2.3`). Ensure the `yq` executable is available in your PATH.

Part 2: Adversarial Log Filtering Pipeline
You must write a shell script at `/home/user/pipeline.sh` that acts as the primary pipeline DAG.
The script must take exactly two arguments:
`./pipeline.sh <input_directory> <output_directory>`

The `<input_directory>` will contain a series of `.json` log files. Each file contains multiple JSON objects (one per line) representing mathematical computation requests. 
Your script must read all `.json` files in the input directory, filter and deduplicate them, and write the surviving valid logs to `<output_directory>/cleaned.json` (one JSON object per line).

Filtering Rules:
You must strictly reject "evil" (malformed, malicious, or corrupted) logs and perfectly preserve "clean" logs. A log is VALID if and only if it meets ALL the following criteria:
1. It is valid JSON.
2. The `duration_ms` field exists, is a number, and is strictly greater than or equal to `0`.
3. The `operation` field exists, is a string, and contains ONLY alphanumeric characters and underscores (regex: `^[a-zA-Z0-9_]+$`). It must not contain spaces, semicolons, shell metacharacters, or be empty.
4. The `status` field exists and is exactly the string `"success"` or `"failure"`.

Deduplication Rule:
If multiple valid logs have the same `request_id`, keep only the FIRST occurrence (based on the order they appear when iterating through the input files alphabetically by filename, and line-by-line within each file).

Part 3: Pipeline Scheduling
Once your script is complete, configure a user-level `cron` job that executes your script every 15 minutes. The cron job should run:
`/home/user/pipeline.sh /app/incoming_logs /home/user/processed_logs`

Make sure `/home/user/pipeline.sh` is executable. You may use `jq`, `yq`, `awk`, `grep`, and standard coreutils within your script.