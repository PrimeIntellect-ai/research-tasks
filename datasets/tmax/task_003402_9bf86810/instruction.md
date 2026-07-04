You are a data engineer tasked with building an ETL pipeline orchestrator in Go. We have a multi-service environment located in `/app/`. There is a startup script at `/app/start_services.sh` that brings up two services:
1. A raw data generator (HTTP service) listening on `127.0.0.1:8081`.
2. A PostgreSQL database listening on `127.0.0.1:5432` (User: `postgres`, Password: `password`, Database: `etl_db`).

Your objective is to write a Go application in `/home/user/etl_pipeline` that orchestrates a multi-stage time-series processing workflow, detects anomalies, and serves the results. 

### Step 1: Initialize the Database
Connect to the Postgres database and create a table named `anomalies`:
```sql
CREATE TABLE IF NOT EXISTS anomalies (
    id SERIAL PRIMARY KEY,
    sensor_id INT,
    timestamp INT,
    value FLOAT,
    rolling_avg FLOAT
);
```

### Step 2: The Go ETL Service
Write a Go web service that listens on `127.0.0.1:9090`. It must expose two endpoints:

**1. `POST /run_pipeline`**
When this endpoint is hit, the pipeline must:
* **Extract**: Fetch the latest bulk time-series data from `http://127.0.0.1:8081/bulk_data`. The response is a JSON array of objects: `{"sensor_id": int, "timestamp": int, "value": float}`.
* **Sample & Stratify**: Group the data by `sensor_id`, sort by `timestamp` ascending. Filter the data to keep *only* the records where the `timestamp` is an even number (e.g., 2, 4, 6...). Discard odd timestamps.
* **Rolling Statistics & Anomaly Detection**: For each `sensor_id`, iterate through the sampled data. Maintain a rolling average of the *previous 2* sampled values (do not include the current value in the average). If there are fewer than 2 previous sampled values, the rolling average is exactly the average of whatever previous values exist (if none exist, the rolling average is 0). 
An **anomaly** is detected if the current value is strictly greater than `1.5 * rolling_avg` (and there is at least 1 previous value).
* **Load**: Bulk import all detected anomalies into the Postgres `anomalies` table. Clear the table before inserting the new run's data to ensure idempotency.

**2. `GET /anomalies`**
Accepts a query parameter `sensor_id`. It must query the Postgres `anomalies` table and return a JSON array of anomalies for that sensor, ordered by `timestamp` ascending. Format: `[{"sensor_id": 1, "timestamp": 4, "value": 10.5, "rolling_avg": 5.0}, ...]`.

### Constraints
* Use Go (1.20+) as your primary language. You may use standard libraries and standard PostgreSQL drivers (e.g., `github.com/lib/pq`).
* Ensure your service is compiled and running in the background. Leave it listening on `127.0.0.1:9090` so our automated verifier can interact with it.
* Run `/app/start_services.sh` to start the background fixtures before testing your pipeline.