You have been tasked with building a data processing pipeline for a Configuration Management system. Configuration changes from various microservices are streamed into log files. These changes arrive with high-precision timestamps and need to be aligned, validated, and processed sequentially.

Your objective is to write a Python script `/home/user/pipeline.py` that processes these configuration logs. 

**Input Data:**
You will find two JSON Lines (JSONL) files:
1. `/home/user/data/service_a.jsonl`
2. `/home/user/data/service_b.jsonl`

Each line contains a JSON object with the following schema:
`{"timestamp": "<ISO8601-string>", "service": "<string>", "key": "<string>", "value": <any>}`

**Pipeline Tasks (DAG Sequence):**
Your script must implement a pipeline that performs the following operations in order:

1. **Extraction & Merging**: Read both files and merge the records.
2. **Timestamp Alignment**: Parse the `timestamp` field (which is in UTC, e.g., `2023-10-25T14:30:07Z`) and align (round down) the time to the nearest 10-second boundary. For example, `14:30:07Z` becomes `14:30:00Z`, and `14:30:19Z` becomes `14:30:10Z`. Store this in a new field `aligned_ts`.
3. **Constraint-based Validation**: Filter the records based on the following strict configuration rules:
   - `memory_limit`: Must be an integer between 128 and 2048 (inclusive).
   - `cpu_cores`: Must be an integer exactly equal to 1, 2, 4, or 8.
   - `maintenance_mode`: Must be a boolean (`true` or `false`).
   *Note: Any record with an unknown key, or a value that does not match these constraints, must be completely discarded.*
4. **Load (Output)**: Write the valid, aligned records to a CSV file at `/home/user/output/valid_configs.csv`. 
   - The CSV must have exactly these headers: `aligned_ts,service,key,value`
   - The rows must be sorted in ascending order by `aligned_ts`, then alphabetically by `service`, then alphabetically by `key`.

**Execution:**
- Write your solution to `/home/user/pipeline.py`.
- Ensure the output directories are created if they do not exist.
- Run your script so that `/home/user/output/valid_configs.csv` is generated successfully.