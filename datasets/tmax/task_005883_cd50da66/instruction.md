You are acting as a Database Administrator optimizing a slow reporting pipeline. Previously, our developers extracted all API request logs into Python to compute response time analytics, which is causing out-of-memory errors. 

Your task is to rewrite the analytics extraction by pushing the analytical computation down to the SQLite database using Window Functions, and implementing proper pagination, parameterization, and schema validation.

We have an SQLite database located at `/home/user/metrics.db` with a table named `api_requests`:
* `id` (INTEGER PRIMARY KEY)
* `endpoint` (TEXT)
* `response_time_ms` (REAL)
* `timestamp` (DATETIME)

Write a Python script at `/home/user/analyze.py` that takes three command-line arguments: `endpoint_name` (string), `limit` (integer), and `offset` (integer). Example usage: `python3 /home/user/analyze.py "/api/users" 10 0`

The script must:
1. Connect to `/home/user/metrics.db`.
2. Execute a **single, parameterized SQL query** that:
   - Filters the data for the given `endpoint` (using parameters, NOT string formatting, to prevent SQL injection).
   - Computes a new column `prev_response_time_ms` which is the `response_time_ms` of the *immediately preceding* request for that same endpoint, ordered chronologically by `timestamp` (using a Window function). If there is no preceding request, this should be `NULL`.
   - Computes a new column `time_diff` which is `response_time_ms - prev_response_time_ms`.
   - Sorts the final output by `timestamp` DESCENDING.
   - Paginates the results using the provided `limit` and `offset` (also parameterized).
3. Extract the results and format them as a list of dictionaries.
4. Validate the resulting Python list against the following strict JSON Schema using the `jsonschema` library (you can install it if needed):
   ```json
   {
     "type": "array",
     "items": {
       "type": "object",
       "properties": {
         "id": {"type": "integer"},
         "endpoint": {"type": "string"},
         "response_time_ms": {"type": "number"},
         "timestamp": {"type": "string"},
         "prev_response_time_ms": {"type": ["number", "null"]},
         "time_diff": {"type": ["number", "null"]}
       },
       "required": ["id", "endpoint", "response_time_ms", "timestamp", "prev_response_time_ms", "time_diff"]
     }
   }
   ```
5. If validation passes, dump the JSON array to `/home/user/output.json`.

Please implement the script and run it for the endpoint `"/api/checkout"` with a limit of `5` and offset of `2`.