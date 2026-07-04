You are tasked with fixing a configuration management data pipeline. The system tracks configuration changes across our infrastructure and aggregates them for auditing. 

There are three services running in the environment, but their configuration is broken, and the core data processing script is missing.

**Part 1: Service Composition & Configuration**
The following services are managed by a startup script but are currently disconnected:
1. **Config Emitter:** A Python service simulating incoming config changes. It reads its target destination from `/home/user/emitter.json`.
2. **Redis Cache:** Running locally.
3. **Audit Dashboard:** A Python Flask app running on port 8080 that provides the final aggregated view. It reads from Redis.

Your task is to fix the flow:
* Modify `/home/user/emitter.json` so that the `"output_type"` is `"redis"`, `"redis_host"` is `"127.0.0.1"`, and `"redis_port"` is `6379`. (Currently, it is misconfigured to write to `/dev/null`).
* Ensure the Audit Dashboard config at `/home/user/dashboard.env` has `REDIS_URL=redis://127.0.0.1:6379/0`.

**Part 2: Data Transformation Script (Bash)**
The configuration logs are pushed into the pipeline in a raw, unnormalized text format. You must write a Bash script at `/home/user/normalize.sh` that reads these raw logs from `stdin` and writes a clean, normalized CSV to `stdout`.

**Input Format (Standard Input):**
Lines of text formatted exactly as:
`YYYY-MM-DD HH:MM:SS | <service_name> | <operation> | <config_key>=<config_value>`
Example: `2023-10-25 14:30:00 | web_server | MODIFY | max_workers=16`

**Transformation Rules & Constraints:**
1. **Timestamp Alignment:** Convert the `YYYY-MM-DD HH:MM:SS` timestamp into a Unix epoch timestamp (UTC).
2. **Data Validation:** 
   * ONLY process lines where `<operation>` is exactly `CREATE`, `MODIFY`, or `DELETE`. Drop all other lines.
   * IF `<config_key>` contains the string `SECRET` (case-insensitive), drop the line completely (do not log it).
3. **Feature Extraction:** Instead of outputting the `<config_value>`, output the integer length (number of characters) of the `<config_value>`.
4. **Sorting & Grouping:** The final output must be sorted numerically by the epoch timestamp (ascending). If timestamps are identical, sort alphabetically by `<service_name>`.
5. **Output Format:** Clean CSV format: `epoch,service_name,operation,config_key,value_length`. No spaces after commas.

Your script must be entirely written in Bash (standard GNU utilities like `awk`, `sed`, `grep`, `date`, `sort` are permitted and expected). Our automated verification will generate thousands of random log lines and pipe them into your script, comparing the output bit-for-bit against a reference implementation.

Please complete the configurations and write the script at `/home/user/normalize.sh`.