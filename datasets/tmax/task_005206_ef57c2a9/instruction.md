You are a data analyst tasked with processing local CSV files and serving the results to an internal dashboard. You have been provided with a local query engine package called `pylitecsv`, but it has a severe bug, and you need to build an API on top of it.

Your workspace contains two CSV files:
1. `/home/user/sales.csv` (Columns: `sale_id`, `product_id`, `amount`, `date`)
2. `/home/user/products.csv` (Columns: `id`, `name`, `category`, `price`)

The `pylitecsv` package is vendored at `/app/pylitecsv-1.0.0`. You are required to use this package to read and join the CSVs. 
However, there is a known issue in the package: when calling its `inner_join(left_table, right_table, left_key, right_key)` method located in `/app/pylitecsv-1.0.0/pylitecsv/engine.py`, it erroneously performs an implicit cross join, resulting in massively duplicated and incorrect rows.

Your tasks:
1. Identify and fix the cross join bug in `/app/pylitecsv-1.0.0/pylitecsv/engine.py`. Ensure it properly enforces the equality between `left_key` and `right_key`.
2. Ensure the package is importable (you may need to install it in development mode or adjust your `PYTHONPATH`).
3. Write a Python script at `/home/user/server.py` that uses Python's built-in `http.server` to expose a REST API.
4. The server must run on `127.0.0.1:8000`.
5. Expose an endpoint `GET /api/merged` that:
   - Uses `pylitecsv` to inner join `sales.csv` and `products.csv` (matching `sales.product_id` to `products.id`).
   - Supports query parameters for pagination: `limit` and `offset`.
   - Supports sorting: `sort` (column name) and `order` (`asc` or `desc`).
   - Supports filtering: `category` (exact match on `products.category`).
   - Returns a JSON response containing a list of dictionaries with the merged row data.

Example request the dashboard will make:
`GET /api/merged?category=Electronics&sort=amount&order=desc&limit=5&offset=0`

Write the server script to be robust, start the server in the background, and redirect its logs to `/home/user/server.log`. Once the server is running and ready, create a file named `/home/user/ready.txt` containing the word `READY`.