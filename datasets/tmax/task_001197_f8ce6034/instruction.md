You are a log analyst investigating intermittent performance spikes across a microservice architecture. 

You have been provided with a raw log file at `/home/user/system_events.log`. This file contains unstructured text with embedded structural elements. 

Each line follows this format:
`[YYYY-MM-DD HH:MM:SS] SVC:<service_name> DEDUPE:<hash> METRICS:<key1>=<val1>,<key2>=<val2>,...`

Your task is to write a Bash script `/home/user/process.sh` that processes this log file and generates a summarized CSV report at `/home/user/metrics_summary.csv`. 

Your script must perform the following pipeline of operations:
1. **Hash-based Deduplication**: Multiple systems may forward the same log event. Filter the logs so that only the *first* occurrence of any `DEDUPE:<hash>` is processed. Discard subsequent duplicates with the same hash.
2. **Timestamp Alignment & Bucketing**: Assume all log timestamps are in UTC. Parse the timestamp and align it to the start of its 15-minute bucket (e.g., `10:05:12` belongs to the `10:00:00` bucket, `10:16:02` belongs to `10:15:00`). Format this bucket start time as an ISO-8601 string (e.g., `2023-11-01T10:00:00Z`).
3. **Structured Extraction & Reshaping**: Extract the service name and the wide-format METRICS field. Reshape the wide metrics (`cpu=12,mem=512`) into a long format.
4. **Aggregation**: For each 15-minute bucket, service, and metric type, calculate the *maximum* recorded value.

**Output Specification:**
The final output file `/home/user/metrics_summary.csv` must be a CSV file with the following header:
`bucket,service,metric,max_value`

Followed by the aggregated data. The rows must be sorted in ascending order by `bucket`, then `service`, and finally `metric`.

**Requirements:**
- You must implement this logic strictly using standard Linux command-line tools and Bash scripting (e.g., `awk`, `sed`, `grep`, `date`, `sort`, `uniq`, etc.). Do not write Python, Perl, or Ruby scripts.
- Ensure your script `/home/user/process.sh` is executable and runs without requiring user interaction. Run it to produce the final CSV.