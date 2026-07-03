You are a localization engineer managing a continuous translation ETL pipeline. Recently, the pipeline has been experiencing network timeouts during the ingestion of translation event logs, causing it to retry and produce duplicate records.

Your task is to build a multi-stage pipeline using Bash and C to deduplicate the events, perform time-based bucketing, compute a rolling aggregation of translation quality, and detect quality anomalies (changepoints).

**Input Data:**
A raw CSV file located at `/home/user/raw_events.csv`.
Columns: `timestamp,translation_id,lang_code,word_count,quality_score`
* `timestamp`: Unix timestamp (integer).
* `translation_id`: Unique identifier for a translation task (string).
* `lang_code`: Target language (string).
* `word_count`: Number of words (integer).
* `quality_score`: Float between 0.0 and 100.0.

Due to retries, there are duplicate rows. The *last* occurrence (closest to the end of the file) of a `translation_id` is the final, correct state. 

**Task Requirements:**

1. **Pipeline Orchestrator (`/home/user/pipeline.sh`)**:
   Write a bash script that:
   - Compiles your C program (`/home/user/analyzer.c`).
   - Deduplicates `raw_events.csv` by keeping only the last occurrence of each `translation_id` (order must be preserved based on the last occurrence's timestamp, so sort the final deduplicated records by `timestamp` ascending).
   - Pipes the cleaned data to your compiled C program.

2. **C Analyzer (`/home/user/analyzer.c`)**:
   Write a C program that reads the deduplicated, sorted CSV data from `stdin` and performs the following:
   - **Time-based bucketing**: Group records into 1-hour buckets. The bucket ID is `timestamp / 3600`.
   - **Aggregation**: Calculate the average `quality_score` for each hour bucket.
   - **Rolling/Windowed Aggregation**: For each hour bucket, calculate the moving average of the `hourly_average` over the last 3 available buckets (including the current bucket). Note: Use the last 3 buckets *present in the data stream*, ignoring time gaps.
   - **Anomaly Detection**: Flag an anomaly (`1`) if a bucket's `hourly_average` is strictly less than its `rolling_average - 5.0`. Otherwise, flag is `0`.

   **Output Format:**
   The C program must print to `stdout`, which your bash script should redirect to `/home/user/anomalies_report.csv`.
   Format per line: `bucket_id,hourly_average,rolling_average,anomaly_flag`
   Format floats to exactly 2 decimal places. 

**Execution:**
Ensure your `pipeline.sh` has executable permissions. Running `./pipeline.sh` must complete the end-to-end process and generate `/home/user/anomalies_report.csv`.