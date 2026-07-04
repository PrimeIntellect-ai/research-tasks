As a compliance officer, you are auditing our cross-system transaction tracking. Our corporate entities are stored in PostgreSQL (representing the ownership hierarchy) and their transactions are logged in MongoDB.

We have a Python script `/app/audit_checker.py` that takes an `--entity-id` and is supposed to return a JSON array of that entity and all its hierarchical descendants, along with their aggregated completed transaction sums from MongoDB.

However, the script is returning massively inflated transaction sums and incorrect entities because the SQL query fetching the descendants contains an implicit cross join, and the script fails to properly map the relational hierarchy to the document store query.

Your task is to fix `/app/audit_checker.py` so that it:
1. Uses a correct Recursive CTE to find the given `--entity-id` and all its descendants (children, grandchildren, etc.) from the `entities` table in PostgreSQL. The table schema is `entities (id VARCHAR PRIMARY KEY, parent_id VARCHAR)`.
2. Retrieves all transactions from the `transactions` collection in MongoDB where the `source_id` is one of the fetched entities AND the `status` is exactly `"COMPLETED"`.
3. Aggregates the total transaction amount per entity. Entities with no completed transactions should have a `total_amount` of `0.0`.
4. Prints exactly and only a JSON array of objects to standard output, sorted by `total_amount` descending, then by `entity_id` ascending. 
   Format example: `[{"entity_id": "CORP_1", "total_amount": 5000.50}, {"entity_id": "CORP_2", "total_amount": 0.0}]`

System Information:
- A `docker-compose.yml` in `/app/` is already running the database services.
- PostgreSQL is available at `localhost:5432` (database: `compliance`, user: `audit`, password: `audit123`).
- MongoDB is available at `localhost:27017` (database: `compliance`).

Do not change the command-line arguments of the script. The automated verification will run your script multiple times with different entity IDs and compare the exact JSON output against a known good oracle. Ensure your output contains no extra debugging print statements.