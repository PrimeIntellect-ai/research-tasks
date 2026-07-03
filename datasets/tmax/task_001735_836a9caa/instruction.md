You are acting as a data analyst. You have been given a Python script `/home/user/report_generator.py` that processes several CSV files (`customers.csv`, `orders.csv`, and `order_items.csv`) by loading them into an in-memory SQLite database and executing a SQL query to generate a report.

Currently, the script is producing massive, incorrect numbers for customer revenue. A quick inspection suggests the SQL query is performing an implicit cross join because the join conditions are completely missing. Furthermore, the report is missing a required ranking metric.

Your task is to fix and enhance the SQL query within `/home/user/report_generator.py` to meet the following requirements:
1. Correctly join the `customers`, `orders`, and `order_items` tables using their logical relationships (`customer_id` and `order_id`).
2. Calculate the `total_revenue` for each customer. Revenue is defined as the sum of `price * quantity` for all their order items.
3. Include a new column called `revenue_rank` that ranks the customers based on their `total_revenue` in descending order (highest revenue is rank 1). You must use the SQL `RANK()` window function.
4. Only include customers who have placed at least one order.
5. Order the final result by `revenue_rank` ascending, and then by `customer_id` ascending to break any ties.
6. The script must output the corrected data to `/home/user/customer_revenue_rank.csv` containing exactly three columns: `customer_id`, `total_revenue`, `revenue_rank`.

Do not change the names of the input CSV files or the output CSV file. You may only modify the SQL query string in the Python script or minor Python logic if necessary to run the query and save it. Once you have fixed the script, execute it to generate the output CSV.