You are a data engineer tasked with building an extraction step for an ETL pipeline. We need to extract data from a relational SQLite database and transform it into a nested JSON document format for ingestion into a NoSQL document database.

The database is located at `/home/user/events.db` and contains two tables:
1. `users` (`id` INTEGER PRIMARY KEY, `name` TEXT, `email` TEXT)
2. `purchases` (`id` INTEGER PRIMARY KEY, `user_id` INTEGER, `amount` REAL, `category` TEXT, `timestamp` DATETIME)

Write a Python script at `/home/user/extract.py` that does the following:
1. Connects to `/home/user/events.db`.
2. Uses `argparse` to accept a parameterized argument `--min-amount` (a float).
3. Executes a single SQL query that safely injects the `--min-amount` parameter. The query must:
   - Filter `purchases` to only include rows where `amount >= min_amount`.
   - Use a Window Function to rank these filtered purchases for each user based on the `amount` in descending order (if amounts are equal, sort by `id` descending).
   - Retrieve ONLY the top 2 highest purchases per user.
   - Join the results with the `users` table to get the user's name and email.
4. Converts the SQL result set into a list of nested JSON documents (a cross-representation mapping from relational to document).
5. Exports the result to `/home/user/output.json`.

The output JSON must be an array of objects, strictly following this schema and sorted by `user_id` in ascending order:
```json
[
  {
    "user_id": 1,
    "profile": {
      "name": "Alice",
      "email": "alice@example.com"
    },
    "top_purchases": [
      {
        "purchase_id": 105,
        "amount": 250.5,
        "category": "electronics"
      },
      ...
    ]
  },
  ...
]
```
Note: 
- `top_purchases` should be sorted by `amount` descending, then `purchase_id` descending.
- If a user has no purchases meeting the criteria, they should NOT appear in the final JSON array.
- Make sure to write valid JSON (use `json.dump` with `indent=2`).

Run your script with `python3 /home/user/extract.py --min-amount 50.0` so that the `/home/user/output.json` file is generated for verification.