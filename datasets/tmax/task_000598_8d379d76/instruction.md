You are an automation specialist tasked with fixing a broken data pipeline. The current ETL pipeline silently drops log entries that contain embedded newlines in the message field, throwing off our time-series analysis. 

Your goal is to parse the messy dataset correctly, perform several specific analytical computations, and serve the cleaned data and metrics via a local REST API.

**1. Data Parsing**
A raw dataset is located at `/home/user/data/messy_logs.csv`. 
The format is CSV with the following columns: `Timestamp,ServerID,CPU,Memory,LogLevel,Message`.
However, the `Message` field is enclosed in double quotes (`"`) and frequently contains embedded newline characters (`\n`). You must parse this file correctly without dropping any rows (a standard line-by-line read will fail).

**2. Data Processing & Computations**
Write a Python script to process the extracted records and calculate the following:
*   **Summary Statistics**: For each `ServerID`, calculate the average `CPU` (float) and the maximum `Memory` (float). 
*   **Time-Series Distance**: Compute the Euclidean distance between the `CPU` utilization time-series of `Server-Alpha` and `Server-Beta`. (Ensure the series are strictly ordered by `Timestamp` before computing the distance. Both servers have exactly the same number of timestamps).
*   **Stratified Sampling**: Extract a stratified sample consisting of exactly 2 records per unique `LogLevel`. To ensure determinism, sort the records for each LogLevel chronologically by `Timestamp`, and take the first 2 records.

**3. API Service Integration**
You must write and start a Python web server (e.g., using Flask or FastAPI) that exposes these results.
*   **Listen Address**: `127.0.0.1`
*   **Port**: `8080`
*   **Authentication**: All endpoints must require an `Authorization` header with the exact value: `Bearer pipe-auth-token-xyz`

**Endpoints**:
*   `GET /stats`: Returns JSON in the format `{"ServerID": {"avg_cpu": float, "max_mem": float}, ...}`.
*   `GET /distance`: Returns JSON in the format `{"euclidean_distance": float}`.
*   `GET /sample`: Returns JSON containing the stratified sample as a list of dictionaries, ordered alphabetically by `LogLevel` and then by `Timestamp`. Keys should be the column names.

Leave the API running in the background so our verification script can query it. You may install any Python packages you need using pip.