You are a data engineer responsible for building a lightweight, Bash-based ETL pipeline to process semi-structured web server logs. You must extract performance metrics, aggregate them into 5-minute time buckets, and orchestrate the workflow using a Makefile DAG.

The raw log file is located at `/home/user/raw_server.log`. 
Each line in the log file follows this general format:
`[YYYY-MM-DD HH:MM:SS] srcIP=<ip> method=<method> endpoint=<endpoint> latency_ms=<latency>`

Example:
`[2023-10-15 14:02:15] srcIP=10.0.0.1 method=POST endpoint=/api/v2/users latency_ms=120`

**Your objective:** Build an ETL pipeline consisting of Bash scripts and a `Makefile` that extracts latency metrics for specific API versions, aggregates them into 5-minute buckets, and outputs a clean JSON file.

**Step 1: Extract (`extract.sh`)**
Write a Bash script `/home/user/extract.sh` that reads `/home/user/raw_server.log` and outputs an intermediate CSV file at `/home/user/extracted.csv`.
- You must use **Regex** to match and extract the `timestamp`, `endpoint`, and `latency_ms`.
- **Filter**: ONLY include log lines where the `endpoint` matches the pattern: exactly `/api/v` followed by a single digit between `1` and `3`, followed by a `/`, followed by one or more lowercase letters or underscores (e.g., `/api/v2/users` or `/api/v1/get_data`). Ignore any other endpoints (like `/api/v4/admin` or `/health`).
- The output `/home/user/extracted.csv` must have the format: `YYYY-MM-DD HH:MM:SS,endpoint,latency_ms` (no headers).

**Step 2: Transform (`transform.sh`)**
Write a Bash script `/home/user/transform.sh` that reads `/home/user/extracted.csv` and outputs an aggregated CSV file at `/home/user/aggregated.csv`.
- **Time-based bucketing**: Floor the timestamp to the nearest 5-minute interval. For example, `14:02:15` becomes `14:00:00`, and `14:07:05` becomes `14:05:00`.
- **Aggregation**: Group the records by the 5-minute bucket and the `endpoint`. Calculate the total `count` of requests and the `average_latency_ms` (integer, rounded down to the nearest whole number).
- The output `/home/user/aggregated.csv` must have the format: `YYYY-MM-DD HH:MM:00,endpoint,count,average_latency_ms` (no headers, sorted chronologically).

**Step 3: Load (`load.sh`)**
Write a Bash script `/home/user/load.sh` that reads `/home/user/aggregated.csv` and outputs a JSON array file at `/home/user/final_metrics.json`.
- The output must be valid JSON matching this structure:
```json
[
  {
    "bucket": "2023-10-15 14:00:00",
    "endpoint": "/api/v2/users",
    "request_count": 2,
    "avg_latency": 125
  }
]
```

**Step 4: Orchestration DAG (`Makefile`)**
Create a `/home/user/Makefile` to orchestrate this pipeline.
- Target `extract` depends on `raw_server.log` and runs `extract.sh` to produce `extracted.csv`.
- Target `transform` depends on `extracted.csv` and runs `transform.sh` to produce `aggregated.csv`.
- Target `load` depends on `aggregated.csv` and runs `load.sh` to produce `final_metrics.json`.
- Target `all` should trigger the entire pipeline from end-to-end to produce `final_metrics.json`.
- Target `clean` should remove all generated CSV and JSON files.

Ensure your scripts are executable. Once written, run `make all` in `/home/user` to generate `/home/user/final_metrics.json`. Do not install external databases; use standard GNU Linux utilities (`grep`, `sed`, `awk`, `jq`, `date`, etc.).