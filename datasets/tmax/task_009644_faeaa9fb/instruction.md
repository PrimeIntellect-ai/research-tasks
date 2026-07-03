You are a Database Administrator tasked with optimizing a critical reporting pipeline for a logistics platform. 

A local SQLite database exists at `/home/user/logistics.db`. It contains the following tables:
- `customers` (id INTEGER PRIMARY KEY, name TEXT)
- `orders` (id INTEGER PRIMARY KEY, customer_id INTEGER, order_date TEXT)
- `order_items` (id INTEGER PRIMARY KEY, order_id INTEGER, price REAL)
- `shipments` (id INTEGER PRIMARY KEY, order_id INTEGER, status TEXT, actual_delivery TEXT, expected_delivery TEXT)

Currently, the reporting query to find top customers affected by delayed shipments is extremely slow because the database lacks appropriate indexes, and the current query formulation requires massive full table scans.

Your task has three parts:

1. **Optimize the Database Layout:**
Analyze the schema and create the necessary indexes to optimize filtering and joining. Save your `CREATE INDEX` statements in `/home/user/indexes.sql`. You must apply these indexes to `/home/user/logistics.db`.

2. **Construct the Optimized Query:**
Write an optimized SQL query in `/home/user/optimized.sql` that retrieves the following schema:
- `customer_id` (INTEGER)
- `customer_name` (TEXT)
- `total_revenue` (REAL) - The sum of all `price` values from `order_items` for this customer across all their orders.
- `latest_order_date` (TEXT) - The maximum `order_date` for this customer.
- `delayed_shipment_count` (INTEGER) - The number of shipments for this customer where `status = 'DELAYED'`.

Conditions:
- Only include customers who have at least one delayed shipment (`delayed_shipment_count > 0`).
- Sort the results by `total_revenue` DESCENDING, then by `customer_id` ASCENDING.
- The query must support pagination using standard SQL `LIMIT` and `OFFSET` clauses. Use the exact placeholders `:limit_val` and `:offset_val` in your `.sql` file for these parameters.

3. **Create the Execution Script:**
Write a bash script at `/home/user/run_report.sh` that takes exactly two arguments: `<limit>` and `<offset>`.
The script must:
- Read `/home/user/optimized.sql`.
- Replace `:limit_val` and `:offset_val` with the provided arguments.
- Execute the query against `/home/user/logistics.db`.
- Output the result strictly as a valid JSON array of objects to `stdout` (e.g., `[{"customer_id": 1, ...}]`). You can use `sqlite3 -json` to achieve this.

Ensure `/home/user/run_report.sh` is executable. You can test your script by running `./run_report.sh 5 0`.