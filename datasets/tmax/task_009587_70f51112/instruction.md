You are a log analyst investigating performance issues across a cluster of servers. You have received a telemetry log file in JSON-Lines format, but it is massive and standard bash utilities are struggling with the mathematical aggregations and unicode escape sequences present in the hostnames (e.g., `web-\u0031`).

Your task is to write a multi-stage data processing pipeline in Go that reads, transforms, and analyzes this telemetry data to detect anomalies. 

**Task Details:**
1. **Input File:** You will process `/home/user/telemetry.jsonl`. Each line is a JSON object with the following fields:
   - `ts` (integer): Timestamp in seconds.
   - `host` (string): The server name, which may contain unicode escape sequences.
   - `cpu` (float): CPU utilization percentage.
   - `latency` (float): Request latency in milliseconds.

2. **Go Program:** Create a Go program at `/home/user/analyze.go`. The program must perform the following pipeline operations:
   - **Parsing:** Parse the JSONL file. Ensure that unicode escape sequences in the `host` field are correctly evaluated (e.g., `web-\u0031` becomes `web-1`).
   - **Parallel Processing:** Group the records by `host`. Process each host's time-series data in parallel using Go routines.
   - **Sorting:** For each host, ensure the records are processed in ascending order of `ts`.
   - **Windowed Aggregation:** Calculate a 5-point Simple Moving Average (SMA) of the `latency` for each host. The SMA for a given record should include that record and the up to 4 preceding records. (If a record is the 3rd for a host, its SMA is the average of the 1st, 2nd, and 3rd records).
   - **Normalization:** Calculate the Z-score for the `cpu` metric for each host based on the entire population of that host's records. 
     - Mean ($\mu$) = sum(cpu) / count(cpu)
     - Population Standard Deviation ($\sigma$) = $\sqrt{\frac{\sum (cpu - \mu)^2}{count}}$
     - Z-score = $(cpu - \mu) / \sigma$. (If $\sigma$ is 0, Z-score is 0).
   - **Anomaly Detection:** An anomaly is defined as a record where the 5-point SMA of `latency` is strictly greater than `150.0` **AND** the `cpu` Z-score is strictly greater than `1.5`.

3. **Output File:** The program must write all detected anomalies to a CSV file at `/home/user/anomalies.csv`.
   - The CSV must have a header: `ts,host,sma_latency,z_cpu`
   - The rows must be sorted in ascending order of `ts`. If timestamps tie, sort by `host` alphabetically.
   - Format `sma_latency` and `z_cpu` to exactly two decimal places (e.g., `152.40`, `1.65`).

4. **Execution:** Build and run your Go program. The final output must reside at `/home/user/anomalies.csv`.

*Note:* Standard Go libraries (`encoding/json`, `math`, `encoding/csv`, `sort`, `sync`, etc.) are entirely sufficient for this task. Do not use external third-party packages.