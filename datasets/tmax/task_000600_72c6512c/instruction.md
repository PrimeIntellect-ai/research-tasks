You are managing a configuration tracking system for a massive ETL pipeline. Recently, a retry bug in the ETL orchestrator caused it to emit duplicate and out-of-order configuration update events.

You need to process the resulting event log to determine the definitive, most recent successful configuration state for each system component.

**Input File:**
`/home/user/etl_config_events.csv`

**Input Format:**
A CSV file without a header. The columns are:
1. `timestamp` (Unix epoch integer)
2. `component_name` (string)
3. `config_hash` (string)
4. `status` (string, either `SUCCESS` or `FAILED`)

**Your Task:**
Write a bash pipeline (using standard tools like `grep`, `awk`, `sort`, etc.) to process this file and extract the final configuration state. 

**Rules:**
1. You must only consider rows where the `status` is `SUCCESS`. Ignore all `FAILED` rows.
2. If there are multiple `SUCCESS` records for the same `component_name`, you must keep only the one with the highest `timestamp`.
3. The output must be formatted as `component_name,config_hash`.
4. The output must be sorted alphabetically by `component_name`.

**Output:**
Save your final results to exactly this file: `/home/user/latest_config.csv`

Ensure you use efficient streaming and sorting commands, as the real files in such systems can be very large.