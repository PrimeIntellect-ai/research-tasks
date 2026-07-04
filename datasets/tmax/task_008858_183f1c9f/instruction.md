You are tasked with building a configuration drift tracking ETL pipeline. A set of remote servers periodically reports their configuration metrics. Occasionally, network retries cause the ingestion system to produce exact duplicate records in the drop folder. 

You must write a C program and a Bash pipeline script to transfer these files, validate and deduplicate the records, join them with a baseline configuration, and compute a rolling mathematical aggregation of the "drift score".

Here are the detailed requirements:

1. **Environment & File Structure**:
   - Remote drop directory: `/home/user/remote_drop/` (contains incoming CSV reports).
   - Local processing directory: `/home/user/incoming/` (you must create this).
   - Output directory: `/home/user/output/` (you must create this).
   - Baseline configuration file: `/home/user/baseline.csv`. Format: `server_id,metric_id,expected_value`.

2. **Pipeline Wrapper Script**:
   Create an executable Bash script at `/home/user/run_pipeline.sh` that performs the following steps in order:
   - Moves all `.csv` files from `/home/user/remote_drop/` into `/home/user/incoming/` (simulating local-remote data transfer).
   - Compiles your C program (`/home/user/etl.c`) into `/home/user/etl_processor` using `gcc`.
   - Executes `/home/user/etl_processor`.
   - Upon successful execution of the C program, writes the exact string `PIPELINE_OK` to `/home/user/output/pipeline.SUCCESS`.

3. **C Program Specifications (`/home/user/etl.c`)**:
   The C program must process the data in `/home/user/incoming/` against `/home/user/baseline.csv`.
   
   **Input Data Format** (`/home/user/incoming/report_*.csv`):
   Columns: `report_id,server_id,timestamp,metric_id,actual_value`
   *Note: Because of ETL retries, there are exact duplicate rows (same report_id, server_id, timestamp, metric_id, and actual_value). You must deduplicate these so that each unique combination is processed exactly once.*

   **Processing Rules**:
   - **Join**: For each valid, deduplicated metric report, find the corresponding `expected_value` in `baseline.csv` (joining on `server_id` and `metric_id`).
   - **Math (Drift)**: Calculate the absolute difference between `expected_value` and `actual_value`. This is the drift for that specific metric.
   - **Aggregation**: Sum the metric drifts for each unique `report_id` to get the `total_report_drift`. Every `report_id` has a single associated `server_id` and `timestamp`.
   - **Windowed Rolling Aggregation**: For each `server_id`, calculate a moving average of the `total_report_drift` over a rolling window of the last **2** reports (ordered strictly by `timestamp` ascending). If it's the first report for a server, the rolling average is simply the total drift of that single report.

   **Output Format**:
   Write the final rolling averages to `/home/user/output/rolling_drift.csv`.
   Format: `server_id,timestamp,rolling_avg_drift`
   - Order the rows primarily by `server_id` (alphabetically ascending), and secondarily by `timestamp` (numerically ascending).
   - Print `rolling_avg_drift` strictly with 1 decimal place (e.g., `15.0`, `7.5`).

You may use standard C libraries (`stdio.h`, `stdlib.h`, `string.h`, `math.h`, etc.). Ensure your code handles basic errors like missing files gracefully. To complete the task, create all necessary scripts/source code and run `/home/user/run_pipeline.sh` successfully.