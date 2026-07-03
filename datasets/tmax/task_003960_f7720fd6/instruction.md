You are a Data Analyst at a retail company. You have been provided with three CSV files containing the company's product catalog and sales data. Your goal is to load this data into an SQLite database, perform schema analysis, write an optimized analytical query to compute trailing revenues, and output a specific report.

The CSV files are located in `/home/user/data/`:
1. `categories.csv`: `category_id`, `category_name`, `parent_category_id` (a hierarchical category structure)
2. `products.csv`: `product_id`, `category_id`, `product_name`
3. `sales.csv`: `sale_id`, `product_id`, `sale_date`, `quantity`, `price`

Your tasks are:
1. **Database Creation & Data Loading:** Load the CSV files into a new SQLite database located at `/home/user/retail.db`.
2. **Optimization:** Analyze the schema and queries you will run, and create necessary indexes to optimize query performance. Save the `CREATE INDEX` SQL statements to `/home/user/indexes.sql`.
3. **Complex Querying:** Write a Python script (`/home/user/analyze.py`) that connects to `/home/user/retail.db` and executes a single query (using CTEs and Window Functions) that does the following:
   - Identifies the 'Electronics' category and ALL of its descendant subcategories (recursively).
   - For all products belonging to these categories, computes the total daily revenue (`quantity * price`) for each `sale_date`.
   - Computes the "trailing 7 sales days revenue" for each product. This is defined as the sum of the daily revenue for the current sale row and the up to 6 preceding sale rows for that product, ordered by `sale_date`.
   - Filters the final results to only include sales dates in October 2023 (from '2023-10-01' to '2023-10-31' inclusive).
   - Outputs the results to `/home/user/electronics_trailing_revenue.csv`.

**Output Format:**
The file `/home/user/electronics_trailing_revenue.csv` must be a CSV with the following columns (with a header row):
`product_id,product_name,sale_date,daily_revenue,trailing_7_sales_revenue`
The output must be ordered by `product_id` ASC, then `sale_date` ASC.

Ensure that your `analyze.py` script runs successfully and produces the required CSV file.