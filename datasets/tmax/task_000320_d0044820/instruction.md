You are a data analyst and backend engineer tasked with building a robust, statistically-informed data ingestion pipeline. We receive batches of transaction data in CSV format, but some batches contain statistical anomalies or malformed schemas.

We have a multi-service infrastructure already partially configured on this machine:
1. **Nginx**: Running as a reverse proxy on port 8080. It routes requests from `http://127.0.0.1:8080/upload` to a backend service at `http://127.0.0.1:9000/upload`.
2. **Redis**: Running locally on port 6379 (no password).
3. **Go Data Ingestion API**: This is the service *you* must build and run. It needs to listen on port 9000.

**Your Objective:**
Write and deploy a Go application (`/home/user/ingest_api/main.go`) that acts as the backend API.

**Step 1: Baseline Statistical Modeling & Caching**
Upon startup, your Go application must read a historical dataset located at `/app/data/historical.csv`. 
The CSV has the following schema: `transaction_id` (string), `timestamp` (int64), `category` (string), `amount` (float64).
For every unique `category` in the historical data, implement a bootstrap sampling method to find the 95% confidence interval of the mean `amount`:
- Draw N=1000 bootstrap samples (each sample must be the same size as the category's row count, drawn with replacement).
- Calculate the mean of each sample.
- Determine the 2.5th percentile (lower bound) and 97.5th percentile (upper bound) of these 1000 means.
- Store these bounds in Redis using the keys `ci_lower_<category>` and `ci_upper_<category>` (as string representations of the floats).

**Step 2: Endpoint Implementation & Data Schema Enforcement**
Implement an HTTP POST endpoint at `/upload` (listening on port 9000). The endpoint will receive a CSV file via a multipart/form-data request (the file field is named `file`).
When a CSV is received:
1. **Schema Enforcement**: Ensure it strictly matches the schema (`transaction_id`, `timestamp`, `category`, `amount`). If any row has a missing column, wrong data type (e.g., `amount` is not a parseable float, `timestamp` is not an integer), or invalid format, immediately reject the file by returning HTTP status `406 Not Acceptable`.
2. **Tabular Aggregation & Anomaly Detection**: For the uploaded file, calculate the mean `amount` for each `category`.
3. **Validation**: Read the cached confidence bounds from Redis for those categories. If the calculated mean for *any* category in the uploaded file falls below its `ci_lower_<category>` or strictly above its `ci_upper_<category>`, reject the file (HTTP `406 Not Acceptable`). If a category in the uploaded file doesn't exist in Redis, reject it (HTTP `406`).
4. If the file passes both schema checks and statistical bounds checks, accept it by returning HTTP status `200 OK`.

**Requirements:**
- Write the application in Go. You may initialize a Go module in `/home/user/ingest_api/`.
- Ensure your Go service remains running in the background listening on port 9000 so that Nginx can route traffic to it.
- Once your service is running and correctly populated Redis, you must create a file `/home/user/ready.txt` containing the word `READY`. An automated verifier will detect this file and begin sending adversarial and clean corpora through the Nginx proxy to test your statistical modeling and schema enforcement.