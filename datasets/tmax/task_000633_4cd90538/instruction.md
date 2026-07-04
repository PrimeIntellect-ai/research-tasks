You are a data engineer tasked with building an ETL pipeline that integrates a legacy C-based data transformation utility with a modern microservice architecture. 

We have incoming partitioned event logs and a static user database. You must build a Bash-based ETL pipeline to clean, join, and transform this data, and then serve the aggregated results via a simple HTTP endpoint.

**System State and Inputs:**
1. **User Data**: Located at `/home/user/data/users.csv` (Headers: `user_id,region,account_type`).
2. **Event Logs**: Partitioned directories under `/home/user/data/logs/` (Format: `YYYY-MM-DD/events.tsv`). Headers: `event_id\tuser_id\ttimestamp\tmetric_value`.
3. **Legacy Binary**: A stripped executable located at `/app/anonymizer`. It reads space-separated `user_id` and `event_id` from standard input and outputs a `secure_token` string. You do not have the source code.

**Your Objectives:**

1. **ETL Script (`/home/user/etl.sh`)**:
   - Write a bash script to process all TSV files in the logs directory.
   - **Outlier/Missing Value Handling**: Discard any log rows where `metric_value` is missing, non-numeric, or less than 0. Discard rows with a missing `user_id`.
   - **Multi-source Data Joining**: Join the cleaned log rows with `users.csv` on `user_id`.
   - **Feature Engineering (via Binary)**: For each valid joined row, pass the `user_id` and `event_id` to `/app/anonymizer` to generate a `secure_token`.
   - **Storage**: Save the final denormalized, transformed dataset into `/home/user/processed/final_dataset.tsv` with columns: `event_id\tuser_id\tregion\tmetric_value\tsecure_token`.
   - **Experiment Tracking**: Append a run summary to `/home/user/etl_runs.log` with the format: `[YYYY-MM-DD HH:MM:SS] Processed <N> valid events`.

2. **Serving Endpoint (`/home/user/serve.sh`)**:
   - Create a background service (using standard Linux tools like `nc` or a simple bash-invoked python server) that listens on `127.0.0.1:8080`.
   - It must handle HTTP GET requests to `/query?region=<REGION_NAME>`.
   - It must ONLY accept requests containing the exact HTTP header: `Authorization: Bearer etl_secret_2024`. Reject others with `401 Unauthorized`.
   - For valid requests, return a `200 OK` HTTP response with a JSON payload containing the sum of `metric_value` for all events in that region, e.g., `{"region": "US-East", "total_metric": 1450.5}`.

Automated tests will run your `etl.sh`, wait for completion, start your `serve.sh`, and issue protocol-level HTTP requests to verify correct transformations and filtering.