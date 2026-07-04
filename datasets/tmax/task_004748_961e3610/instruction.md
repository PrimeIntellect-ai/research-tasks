You are a data analyst acting as a backend engineer. We need to process some organizational data and expose the results via a secure API. 

You have been provided with two CSV files:
1. `/app/employees.csv`: Contains `emp_id, manager_id, dept_id, name`. (The CEO has no `manager_id`).
2. `/app/transactions.csv`: Contains `tx_id, emp_id, amount, timestamp`.

We also have a scanned configuration snippet at `/app/system_config.png`. This image contains two critical pieces of information you must extract (using OCR, e.g., `tesseract`):
- An API Token (Format: `API_TOKEN=<token>`)
- A minimum transaction threshold (Format: `MIN_TX_THRESHOLD=<number>`)

Your task is to write and run a Rust web service (using a framework like `axum` or `actix-web`) that listens on `127.0.0.1:8080`. 

The service must implement the following:
1. **Data Processing:** Upon startup, the service should read the CSVs and build an in-memory graph or load them into an embedded database (like SQLite/DuckDB). 
2. **Recursive/Hierarchical Aggregation:** For any given employee, their "total team volume" is the sum of all transaction amounts belonging to them AND all of their direct and indirect subordinates recursively.
3. **Filtering:** Only transactions with an `amount` strictly greater than the `MIN_TX_THRESHOLD` (extracted from the image) should be included in *any* calculation.
4. **Endpoint:** Expose a `GET /dept-top-earners?dept_id=<ID>` endpoint.
5. **Authentication:** The endpoint must strictly require an HTTP header `Authorization: Bearer <API_TOKEN_FROM_IMAGE>`. Return a `401 Unauthorized` if missing or incorrect.
6. **Windowing/Analytics Response:** The endpoint must return a JSON response containing the top 3 employees *in the requested department*, ranked descending by their "total team volume". If there is a tie, sort by `emp_id` ascending.
   
The JSON response format must be exactly:
```json
{
  "department": "<dept_id>",
  "top_earners": [
    {
      "emp_id": "<emp_id>",
      "team_volume": 15000.50
    },
    ... (up to 3)
  ]
}
```

Make sure your Rust project is initialized in `/home/user/app-service` and the server is actively running in the background so it can be queried by our automated verification suite.