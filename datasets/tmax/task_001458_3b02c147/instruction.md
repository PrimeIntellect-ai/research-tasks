You are a Database Reliability Engineer (DBRE) responsible for validating our nightly database backups. 

We have a vendored Python package located at `/app/sqlite-backup-validator-1.0` that we use to run consistency checks and generate aggregation summaries from our SQLite backups. 

Currently, the validator is broken:
1. When we run it against our generated test backup database, it either hangs indefinitely, runs out of memory, or returns wildly incorrect aggregate values. We suspect there is a massive implicit cross join in the SQL query located inside the package's `validator.py`.
2. The `Makefile` in the package seems to have a hardcoded wrong path that ignores environment variables.

Your task:
1. Generate the test backup database by running the pre-existing script: `python3 /app/setup_test_db.py`. This will create a SQLite database at `/home/user/backup.db` containing `customers`, `orders`, and `items` tables.
2. Inspect and fix the vendored package at `/app/sqlite-backup-validator-1.0`. 
   - Fix the `Makefile` so that running `make validate DB_PATH=/home/user/backup.db` correctly passes the database path to the python script.
   - Fix the SQL query in `validator.py` to remove the implicit cross join. The query is supposed to calculate the total order amount and total item count per customer. Use proper explicit `JOIN` syntax.
3. Run the fixed package using `make validate DB_PATH=/home/user/backup.db`.
4. Ensure the output is saved to `/home/user/validation_summary.json`. 

The output JSON should be a list of dictionaries with this exact format:
```json
[
  {
    "customer_id": 1,
    "customer_name": "Customer_1",
    "total_order_amount": 150.50,
    "total_items": 12
  },
  ...
]
```

To succeed, your generated `validation_summary.json` must exactly match the true aggregates of the database, meaning the Mean Absolute Error (MAE) evaluated by our verification script must be `0.0`.