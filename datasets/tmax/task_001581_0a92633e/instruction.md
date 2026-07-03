You are a database administrator tasked with optimizing and parameterizing our reporting queries. 

We have an SQLite database located at `/home/user/ecommerce.db` with the following schema:
- `users` (id INTEGER PRIMARY KEY, name TEXT)
- `orders` (id INTEGER PRIMARY KEY, user_id INTEGER, order_date DATE)
- `order_items` (id INTEGER PRIMARY KEY, order_id INTEGER, product_id INTEGER, quantity INTEGER)
- `products` (id INTEGER PRIMARY KEY, name TEXT, category TEXT, price REAL)

Your objective is to create a reliable, parameterized reporting script in pure Bash. 

Here are your requirements:
1. Write a Bash script at `/home/user/run_report.sh` that takes exactly one argument: a `USER_ID`.
2. The script must query the database to find the total amount spent by that user in each product category.
3. The output must be printed to `stdout` in pure CSV format with no headers: `category,total_spend`. 
   - `total_spend` must be formatted to exactly 2 decimal places.
   - The results must be ordered by `total_spend` descending, and then by `category` ascending alphabetically.
4. To safely construct the SQL query without nasty string concatenation, you must use the Mustache templating tool `mo`. 
   - We have vendored the `mo` package source code under `/app/mo-3.0.2/`.
   - Before you can use it, you will notice it is currently broken. A junior developer accidentally introduced a bug into the `/app/mo-3.0.2/mo` script while trying to modify shell options. You must diagnose and fix this perturbation so the templating engine works correctly.
   - Write your SQL template using standard Mustache syntax (e.g., `{{USER_ID}}`) and save it to `/home/user/query.sql.mo`. Your `/home/user/run_report.sh` script should use the fixed `mo` executable to render the query and pipe it to `sqlite3`.

Ensure your script is executable (`chmod +x /home/user/run_report.sh`). Your script will be tested against hundreds of random user IDs to ensure absolute bit-exact equivalence with our internal reporting oracle.