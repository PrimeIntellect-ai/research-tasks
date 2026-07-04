You are stepping into a data pipeline issue. A previous data analyst wrote a Python script at `/home/user/generate_report.py` that processes three CSV files (`customers.csv`, `products.csv`, and `sales.csv`) by loading them into an in-memory SQLite database and running an aggregation query.

Unfortunately, the script has a critical flaw: the query runs incredibly slowly on larger datasets, and the aggregated `total_sales` numbers are massively inflated, indicating a logical error in how the tables are combined.

Your task is to fix and optimize this data pipeline:
1. Identify and fix the logical bug in the SQL query inside `/home/user/generate_report.py`. The query should calculate the total sales amount per customer region and product category.
2. Optimize the query by adding SQL statements in the script to create appropriate indexes on the `sales` table before the `SELECT` query runs. You must index the foreign keys used in the joins.
3. Add code to the script to capture the `EXPLAIN QUERY PLAN` for your fixed `SELECT` query. Save the raw output of this explain plan to `/home/user/query_plan.txt`.
4. Modify the script so that instead of just printing the results, it exports the correct aggregated results to `/home/user/regional_sales_report.json`. The JSON file must be an array of objects, with each object formatted exactly like this:
   `{"region": "North", "category": "Electronics", "total_sales": 500.0}`

Run your fixed script to generate both `/home/user/query_plan.txt` and `/home/user/regional_sales_report.json`.