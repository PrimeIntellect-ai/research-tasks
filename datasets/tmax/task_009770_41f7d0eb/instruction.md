You are a database administrator tasked with optimizing a slow query pipeline that is causing concurrency issues in our backend. Our system uses a SQLite database located at `/home/user/ecommerce.db`. Recently, a new background writer process has been added, and because our read queries are currently doing full table scans, they hold read locks for too long, leading to "database is locked" errors and deadlocks.

Your objective is to optimize the database schema with the correct index strategy and write a robust Bash script that retrieves paginated results securely.

Task Requirements:

1. **Index Strategy Design:**
   Analyze the following query pattern and create the most optimal covering index (or indexes) in `/home/user/ecommerce.db` to prevent full table scans and avoid in-memory sorting:
   `SELECT order_id, order_date, amount FROM orders WHERE customer_id = ? AND status = ? ORDER BY order_date DESC LIMIT ? OFFSET ?`
   
2. **Bash Script Construction:**
   Create a script at `/home/user/get_orders.sh` that takes exactly four arguments:
   `$1`: customer_id (string)
   `$2`: status (string)
   `$3`: limit (integer)
   `$4`: offset (integer)

3. **Query Execution & Concurrency:**
   Inside your Bash script, execute the query against `/home/user/ecommerce.db`. 
   - To handle the concurrency deadlocks, you must configure the SQLite connection to wait up to 5000 milliseconds when the database is locked before failing.
   - You must use SQLite CLI parameter binding (e.g., using `.parameter set`) to prevent SQL injection and properly bind `$1` and `$2`. DO NOT directly interpolate `$1` and `$2` into the SQL string.
   - `$3` and `$4` can be safely interpolated as they should be validated as integers within your script (exit with code 1 if they are not strictly integers).

4. **Result Processing & Formatting:**
   - The output of the script must be standard CSV format, including the header row: `order_id,order_date,amount`.
   - Output the CSV directly to `stdout`.

Constraints:
- Do not modify the existing data or table schema in `/home/user/ecommerce.db` other than adding your index(es).
- Ensure the script has executable permissions (`chmod +x`).
- The SQLite table is named `orders` with columns: `order_id`, `customer_id`, `order_date`, `status`, `amount`.