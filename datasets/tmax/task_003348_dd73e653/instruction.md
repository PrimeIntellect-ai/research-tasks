You are an analyst tasked with building a lightweight ETL pipeline and an API to process incoming data batches. We have a legacy scoring algorithm that has been compiled into a stripped executable, and we need to wrap it in a modern service while tracking experiment metrics.

Here are the requirements:

1. **The Data & The Oracle**:
   - You will find raw CSV files in `/home/user/data/` (e.g., `batch1.csv`, `batch2.csv`). Each CSV has a header: `id,v1,v2,v3`.
   - There is a legacy stripped binary located at `/app/score_calc`. It takes exactly three floating-point numbers as positional arguments and prints a single numeric score to standard output (e.g., `/app/score_calc 1.5 2.0 3.1`).

2. **The ETL Pipeline (Must be written in Bash)**:
   - Create a Bash script at `/home/user/pipeline.sh` that takes a batch name (e.g., `batch1`) as an argument.
   - The script must read `/home/user/data/<batch_name>.csv`.
   - For each row (skipping the header), it must invoke `/app/score_calc` with the values `v1`, `v2`, and `v3`.
   - It must compute the **average score** for the batch.
   - It must count the number of **anomalies**. An anomaly is defined as any score strictly greater than `5.0`.
   - **Experiment Tracking**: The script must append a line to `/home/user/tracking.log` in the exact format: `[<timestamp>] BATCH=<batch_name> AVG=<average_score> ANOMALIES=<count>` (where `<timestamp>` is standard ISO 8601 UTC time, e.g., `2023-10-25T14:30:00Z`).

3. **The API Service**:
   - Create and run an HTTP service listening on `127.0.0.1:8080`. You may use Python (e.g., Flask/http.server) or any tool available to serve this, but the core processing MUST invoke your `/home/user/pipeline.sh`.
   - The service must expose a `GET /process?batch=<batch_name>` endpoint.
   - Upon receiving a request, it should execute the ETL pipeline for the specified batch.
   - It must return a JSON response with status code 200:
     `{"batch": "<batch_name>", "average_score": <average_score>, "anomalies": <count>}`
   - The `average_score` in the JSON should be rounded to exactly 2 decimal places.

Ensure your service is running in the background and listening on port 8080 when you finish the task. Do not assume the exact number of rows in the CSV files.