You are acting as a database administrator for a small e-commerce platform. You have been given a SQLite database file at `/home/user/ecommerce.db` which contains tables for `users`, `products`, `orders`, and `order_items`. The database currently has no indexes other than primary keys, making analytical queries slow.

Your task consists of three parts:

1. **Reverse Engineer and Optimize (Index Strategy Design)**
   Analyze the schema of `/home/user/ecommerce.db`. Identify the foreign key relationships and the columns that would be heavily used for filtering when querying for items ordered in a specific product category within a specific date range. 
   Create a SQL script at `/home/user/optimize.sql` that creates at least 4 indexes to optimize this specific querying pattern (indexes on foreign keys used in the joins, and indexes on the category and date columns). Apply this script to the database.

2. **Data Querying (Parameterized Query Construction)**
   Write a Python script at `/home/user/export.py` that connects to the database and extracts order information.
   The script must accept exactly three command-line arguments: `category`, `start_date`, and `end_date` (dates in YYYY-MM-DD format).
   It must use highly secure parameterized SQL queries (do not use string formatting for the variables) to prevent SQL injection.
   The query should retrieve all items purchased that belong to the given `category`, where the `orders.order_date` is between `start_date` and `end_date` (inclusive).

3. **Format Conversion (Export)**
   The Python script must export the results to `/home/user/output.json` as a JSON array of objects. 
   Each object must have the exact following keys:
   - `user_name` (from users)
   - `email` (from users)
   - `order_date` (from orders)
   - `product_name` (from products)
   - `quantity` (from order_items)
   
   The exported JSON array must be sorted by `order_date` ascending, then `product_name` ascending, and finally `user_name` ascending.

After writing your scripts, run your Python script using the following parameters:
`python3 /home/user/export.py "Electronics" "2023-01-01" "2023-12-31"`

Ensure the final `output.json` is correctly formatted and the database contains the new indexes.