You are an automation specialist tasked with building a robust data processing workflow and serving the results via a REST API. We have a daily pipeline that processes server metrics, but the configuration details for today's run were provided only as a screenshot.

Here are your instructions:

1. **Extract Configuration**: 
   There is an image at `/app/pipeline_config.png`. Use OCR (e.g., `tesseract`) to read the text from this image. It contains two important configuration values:
   - `PIPELINE_ID`: A secret token used for API authentication.
   - `INTERVAL`: A time interval string (e.g., "15min", "1H") that must be used for time-based bucketing.

2. **Data Processing Workflow**:
   We have several messy CSV log files located in `/app/data/` (e.g., `logs_part1.csv`, `logs_part2.csv`). The CSVs contain the following columns: `timestamp` (ISO 8601 format), `server_id`, `cpu`, and `mem`.
   - **Union & Sort**: Read and combine all CSV files in the `/app/data/` directory. Sort the combined data chronologically by `timestamp`.
   - **Imputation**: Some rows have missing `cpu` or `mem` values. For each `server_id`, perform linear interpolation based on the timestamp sequence to fill in the missing numerical values. Forward-fill or backward-fill any remaining NaNs at the boundaries.
   - **Aggregation**: Group the data by `server_id` and bucket the timestamps using the `INTERVAL` extracted from the image. For each bucket, calculate the mean `cpu` and mean `mem`.

3. **Serve the Data**:
   Create and start a Python HTTP server (e.g., using Flask or FastAPI) listening on `127.0.0.1:8080`.
   - **Endpoint**: `GET /api/metrics`
   - **Query Parameter**: `server_id` (e.g., `?server_id=srv-A`)
   - **Authentication**: The API MUST require an `Authorization` header formatted as `Bearer <PIPELINE_ID>` (using the ID extracted from the image). Return a 401 Unauthorized if the token is missing or incorrect.
   - **Response Format**: A JSON array of objects for the requested `server_id`, sorted chronologically by the bucketed timestamp. Each object must have the keys:
     - `timestamp`: The start time of the bucket (ISO 8601 format string, e.g., "2023-10-01T00:00:00").
     - `cpu`: The mean CPU usage (float, rounded to 2 decimal places).
     - `mem`: The mean memory usage (float, rounded to 2 decimal places).

Ensure the server is running in the background or as a final blocking process so the automated verifier can query it. You can write your logic in a Python script (e.g., `/home/user/pipeline.py`) and execute it.