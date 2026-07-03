You are an AI assistant tasked with building an ETL pipeline for a configuration management system. We receive periodic configuration snapshots from our server fleet, but the reporting agents are buggy: they report configurations out-of-order, use inconsistent timestamp formats, and report redundant states even when nothing has changed.

Your goal is to process the raw snapshot data and generate a standardized CSV report of **configuration drifts** (changes).

**Input Data:**
You will find a JSONLines file at `/home/user/raw_configs.jsonl`. Each line is a JSON object representing a configuration snapshot from a host. 
Fields included: `host`, `timestamp`, `cpu_cores`, `ram_gb`, `max_conns`.
The `timestamp` field contains mixed formats (e.g., Unix epochs as integers, ISO8601 strings, and custom strings like "YYYY-MM-DD HH:MM:SS -0700").

**Processing Requirements:**
1. **Timestamp Normalization**: Convert all timestamps to strict UTC ISO8601 format: `YYYY-MM-DDTHH:MM:SSZ`.
2. **Alignment & Deduplication**: For each `host`, process the snapshots in strict chronological order. 
3. **Wide-to-Long Reshaping**: The original data is "wide" (all parameters in one object). You must reshape this into a "long" format that only records *changes*.
4. **Baseline**: The chronologically earliest snapshot for a given `host` establishes its baseline state. **Do not** output any changes for this baseline snapshot.
5. **Drift Detection**: For all subsequent snapshots of a host, compare the parameters (`cpu_cores`, `ram_gb`, `max_conns`) to the host's *most recently known state*. If a parameter has changed, emit a record. If the snapshot is completely identical to the previous chronological state, ignore it.

**Output Format:**
Create a CSV file at `/home/user/config_drifts.csv` with the exact following header:
`host,timestamp,parameter,old_value,new_value`

Sort the final CSV by `host` (ascending), then `timestamp` (ascending), then `parameter` (alphabetically ascending).

Ensure the pipeline is efficient and can be executed via terminal commands or scripts (Python, Bash, jq, etc. are all allowed).