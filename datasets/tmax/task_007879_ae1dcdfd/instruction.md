You are a data engineer debugging an ETL pipeline. 

In `/home/user/etl`, there is a SQLite database `source.db` containing two tables: `customers` (id, name, region) and `orders` (id, customer_id, amount, date). 
There is also a Python script `migrate.py` designed to extract data for a specific date and map it into a document-oriented JSONL format for ingestion into a NoSQL database. 

However, the pipeline is currently broken. The SQL query in `migrate.py` contains an implicit cross join, resulting in incorrect, duplicated data. 

Your tasks:
1. Fix the SQL query in `/home/user/etl/migrate.py` so it properly joins `customers` and `orders`.
2. Update the script to use a secure, parameterized query to filter orders by the date provided as the first command-line argument.
3. Fix the cross-representation mapping in the script so it outputs one JSON object per customer. Each document must have the following exact schema:
   `{"customer_id": <int>, "name": "<string>", "region": "<string>", "orders": [{"order_id": <int>, "amount": <float>}, ...]}`
   Customers with no orders on that date should NOT be included in the output.
4. Run your fixed `migrate.py` script for the date `2023-10-01`. It should output to `/home/user/etl/output.jsonl` (one JSON object per line).
5. Next, write a NoSQL aggregation script (you can use Python or Node.js) named `/home/user/etl/aggregate.py` that reads `/home/user/etl/output.jsonl` and simulates an aggregation pipeline. It must calculate the total order amount per region for this date and write the results to `/home/user/etl/revenue_by_region.json`.
   The final JSON file must be a single JSON object mapping region names to total amounts, exactly like this: `{"North": 150.50, "South": 200.00}`

Do not install any external databases like MongoDB; simulate the NoSQL document operations purely via JSON handling in Python or Node.js.