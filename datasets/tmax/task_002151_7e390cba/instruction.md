You are a data engineer building an analytical ETL pipeline. 

We have three raw data files in `/home/user/`:
1. `customers.csv` (columns: `customer_id`, `name`, `signup_date`)
2. `transactions.csv` (columns: `tx_id`, `customer_id`, `tx_date`, `amount`)
3. `calls.csv` (columns: `call_id`, `customer_id`, `call_date`, `duration_seconds`)

There is also an audio file at `/app/requirements.wav` provided by the product manager. It contains dictated requirements for the API authentication token and the rolling window timeframe for our analytics. 

Your task involves the following phases:
1. **Audio Extraction:** Transcribe `/app/requirements.wav` to discover the required API access token and the rolling window duration (in days).
2. **Database Setup & Indexing:** Write a Python script to ingest the three CSV files into an SQLite database located at `/home/user/analytics.db`. Design and execute an index strategy to optimize for joins on `customer_id` and temporal ordering on `tx_date` and `call_date`.
3. **Complex Analytical Query:** Construct a SQL query using Window Functions to calculate the rolling sum of `amount` for each customer over the last *N* days (where *N* is the window duration from the audio) leading up to their most recent transaction. Join this with a subquery that retrieves the `duration_seconds` of their most recent call.
4. **API Service:** Build a Python HTTP server (e.g., using FastAPI or Flask) listening on `127.0.0.1:9090`. 
    - Expose a `GET /insights` endpoint.
    - Protect the endpoint by requiring the header `X-API-Token` with the exact token extracted from the audio.
    - Execute the analytical query and strictly validate the output schema. The endpoint must return a JSON array of objects with exactly these keys: `{"customer_id": int, "rolling_amount": float, "latest_call_duration": int}`. Do not include customers who have no transactions or calls.

Leave the API running in the background so the validation suite can test it.