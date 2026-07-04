You are a data analyst managing a server metrics ETL pipeline. The previous iteration of this pipeline had a critical flaw: it simply appended data to the output file, so whenever the orchestrator retried the job after a transient failure, it produced thousands of duplicate records.

You need to write a robust, idempotent ETL pipeline that extracts, reshapes, joins, and normalizes server metrics.

You are provided with three input files in `/home/user/data/`:
1. `raw_logs.txt`: A unstructured log file containing metrics in a "long" format. 
   Example lines:
   `[2023-10-01T10:00:00Z] node_ip=10.0.0.1 type=metric key=cpu val=500`
   `[2023-10-01T10:00:00Z] node_ip=10.0.0.1 type=metric key=mem val=8000`
   *(Note: The log file contains some exact duplicate lines due to a bug in the logging agent. You must ignore any exact duplicate lines).*
2. `capacities.csv`: Contains the maximum capacity for each node.
   Columns: `ip_address, max_cpu, max_mem`
3. `locations.csv`: Contains the physical location of each node.
   Columns: `ip_address, datacenter`

Your task:
1. Write a Python script `/home/user/etl.py` that processes these files.
2. The script must parse the unstructured text to extract the `timestamp`, `ip_address`, `key`, and `val`.
3. Reshape the data from long format (where `cpu` and `mem` are on separate rows) into a wide format (where each row represents a unique combination of `timestamp` and `ip_address`, with separate columns for `cpu` and `mem`).
4. Join the reshaped data with `capacities.csv` and `locations.csv`.
5. Normalize the metrics: Create `cpu_percent` and `mem_percent` by dividing the extracted `cpu` and `mem` values by their respective `max_cpu` and `max_mem` capacities, then multiplying by 100. Round these percentages to 1 decimal place.
6. The script must output the final data to `/home/user/output/final_metrics.csv` with the following headers:
   `timestamp, ip_address, datacenter, cpu_percent, mem_percent`
7. The output CSV must be sorted chronologically by `timestamp` ascending, and then by `ip_address` ascending.
8. Create a `/home/user/Makefile` with a target called `run` that executes your Python script. 
9. **Idempotency Requirement**: Running `make run` multiple times must result in the exact same `final_metrics.csv` file without any duplicated rows. Overwriting is perfectly acceptable.

Please complete the task.