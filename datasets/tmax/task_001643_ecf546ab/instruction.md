You are a data analyst responsible for processing a batch of daily server metric CSVs. You need to build a mini-ETL pipeline in Python that orchestrates a set of tasks using a Directed Acyclic Graph (DAG) approach, logs the execution, loads the data into a database, detects anomalies, and exports the results.

The CSV files are located in `/home/user/data/` and follow the format:
`timestamp,cpu_usage,memory_mb,network_tx_kb`
(Note: `timestamp` is an ISO 8601 string like `2023-10-01T14:00:00Z`. There may be multiple readings per day).

Write a Python script `/home/user/pipeline.py` that fulfills the following requirements:

1. **DAG Orchestration**:
   - Implement a simple DAG resolver in your script that takes tasks and their dependencies and executes them in valid topological order.
   - The tasks are: `init_db`, `load_data`, `detect_anomalies`, `export_results`.
   - Dependencies: 
     - `load_data` depends on `init_db`.
     - `detect_anomalies` depends on `load_data`.
     - `export_results` depends on `detect_anomalies`.

2. **Task Implementations**:
   - `init_db`: Creates a SQLite database at `/home/user/metrics.db` with a table `server_metrics` (`timestamp` TEXT, `cpu_usage` REAL, `memory_mb` REAL, `network_tx_kb` REAL). Drops the table first if it exists.
   - `load_data`: Reads all CSV files in `/home/user/data/` (e.g., `metrics_1.csv`, `metrics_2.csv`) and bulk inserts their rows into the `server_metrics` table.
   - `detect_anomalies`: Queries the database to calculate the daily average `cpu_usage`. An "anomaly" is defined as any day where the average `cpu_usage` is strictly greater than 1.5 times the average `cpu_usage` of the *immediately preceding day* present in the dataset. Return a list of anomaly dates (format: `YYYY-MM-DD`).
   - `export_results`: Takes the list of anomaly dates from the previous step and writes it to `/home/user/anomalies.json` in the format: `{"anomalies": ["2023-10-04"]}`.

3. **Logging & Monitoring**:
   - Configure Python's standard `logging` module to write to `/home/user/pipeline.log`.
   - The format must be exactly: `%(levelname)s:%(name)s:%(message)s`.
   - The logger name must be `DAG`.
   - Before executing a task, log: `Starting task <task_name>` (at INFO level).
   - After successfully completing a task, log: `Completed task <task_name>` (at INFO level).

Execute your script to produce the database, the log file, and the anomalies JSON file.