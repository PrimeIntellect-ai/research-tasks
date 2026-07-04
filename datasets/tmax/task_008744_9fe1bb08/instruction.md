You are assisting a compliance officer auditing an internal financial system. We need to identify anomalous transactions that deviate significantly from a user's recent spending baseline.

You have been provided with a SQLite database containing transaction records at `/home/user/transactions.db`. 

The database has a single table:
`transactions` (`id` INTEGER PRIMARY KEY, `user_id` TEXT, `timestamp` INTEGER, `amount` REAL)

Your task is to write and execute a Python data pipeline that does the following:
1. **Window Function Analysis**: Query the SQLite database to compute a rolling moving average of the `amount` for each user. 
   - The moving average must be calculated over a window of exactly 5 transactions: the current transaction and the 4 immediately preceding transactions for the same `user_id`, ordered by `timestamp` ascending.
   - Ignore transactions that do not have at least 4 preceding transactions (i.e., do not evaluate the first 4 transactions for any user).
2. **Flag Anomalies**: Filter the results to find anomalies. An anomaly is defined as any transaction where the `amount` is strictly greater than `2.0 * moving_average`.
3. **Schema Validation**: Your Python script must validate the flagged records to ensure they strictly conform to this JSON schema (you may use Pydantic, jsonschema, or custom validation):
   - `transaction_id`: integer
   - `user_id`: string
   - `timestamp`: integer
   - `amount`: float
   - `moving_average`: float (rounded to exactly 2 decimal places)
4. **Export**: Save the validated anomalies as a JSON array to `/home/user/flagged_anomalies.json`. The JSON file should be pretty-printed.

Ensure your pipeline uses SQLite's window functions (e.g., `AVG() OVER (...)`) directly in the query to perform the aggregation before fetching the results into Python for validation and serialization.