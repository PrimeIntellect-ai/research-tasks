You are acting as a database administrator. We have a SQLite database located at `/home/user/ecommerce.db` containing two tables:
- `customers` (`id` INTEGER PRIMARY KEY, `name` TEXT)
- `orders` (`id` INTEGER PRIMARY KEY, `customer_id` INTEGER, `amount` REAL, `order_date` DATE)

Currently, we are trying to find the top 5 customers by total spending, including their overall rank and total amount. Our analysts have been using slow correlated subqueries.

Your task is to write a Python script at `/home/user/optimize.py` that does the following:
1. Connects to `/home/user/ecommerce.db`.
2. Creates an appropriate index on the `orders` table to optimize grouping by `customer_id`.
3. Constructs a parameterized query using SQLite Window Functions (`RANK()` and aggregation) and CTEs to calculate the total amount spent by each customer, rank them descending by total spending, and return the `name`, `total_amount`, and `rank` for a given limit (parameterized).
4. Executes the query with the limit parameter set to 5.
5. Saves the result as a list of dictionaries to `/home/user/top_customers.json`. Example format: `[{"name": "Alice", "total_amount": 1500.5, "rank": 1}, ...]`.
6. Executes `EXPLAIN QUERY PLAN` on your optimized query and saves the textual output to `/home/user/query_plan.txt`.

Ensure your Python script creates the database connection, performs the index creation, runs the queries, and writes the output files. Run your script to generate the final output files.