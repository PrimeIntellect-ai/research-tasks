You are acting as a Database Administrator for a small e-commerce platform. Our reporting system uses a Python script to calculate the top spenders in specific product categories. However, the current script (`/home/user/generate_report.py`) is causing "database is locked" errors and pseudo-deadlocks because the query it runs is extremely inefficient. It uses correlated subqueries and the database (`/home/user/ecommerce.db`) is missing critical indexes.

Your task is to optimize this reporting process. 

Specifically, you must:
1. Analyze the schema of `/home/user/ecommerce.db`.
2. Create a SQL file at `/home/user/schema_optimization.sql` containing the `CREATE INDEX` statements necessary to speed up joins involving users, orders, order items, and product categories. Execute this script against the database.
3. Rewrite the query inside `/home/user/generate_report.py`. Replace the inefficient correlated subquery with a properly structured query using `JOIN`, `GROUP BY`, and parameterized inputs. The script currently accepts a category name as an argument and outputs a JSON file.
4. Run the updated Python script for the category "Electronics" to produce the output file `/home/user/report.json`.
   Run it as: `python3 /home/user/generate_report.py "Electronics"`

Requirements for `/home/user/generate_report.py`:
- Do not change the JSON output structure or filename (`report.json`).
- Ensure the query uses standard JOINs instead of running a subquery for every user.
- The script must remain parameterized to prevent SQL injection (do not hardcode 'Electronics' into the SQL string).

Requirements for `/home/user/schema_optimization.sql`:
- It must contain only standard SQLite `CREATE INDEX` statements.
- You must index the foreign keys used in the relationships between `orders`, `order_items`, and `products`, as well as the `category` column in `products`.

Once you are done, the file `/home/user/report.json` must exist, contain the correct top 5 users, and the database must contain your new indexes.