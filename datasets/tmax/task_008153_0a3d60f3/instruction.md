You are a data engineer building an ETL pipeline to analyze accessory product sales based on a product knowledge graph. 

You have been provided with a SQLite database at `/home/user/ecommerce.db` containing two tables:
1. `sales` (`transaction_id` INTEGER, `product_id` TEXT, `sale_date` DATE, `amount` REAL)
2. `product_graph` (`src_product_id` TEXT, `dst_product_id` TEXT, `relationship_type` TEXT)

Your goal is to write a Python script at `/home/user/pipeline.py` that performs the following tasks:
1. Connects to `/home/user/ecommerce.db`.
2. Executes SQL to create optimal indexes on both tables to speed up filtering by `relationship_type` and joining on `product_id` and `sale_date`. Ensure you create at least one index for the `sales` table and one for the `product_graph` table.
3. Executes a single SQL query (using CTEs and Window Functions) that:
   - Uses the `product_graph` to find all accessory relationships (where `relationship_type` is exactly `'is_accessory_of'`). In this relationship, `src_product_id` is the accessory and `dst_product_id` is the base product.
   - For each accessory product, calculates the daily total sales `amount`.
   - Computes a rolling 3-day average of the daily total sales for each accessory product. The 3-day window should include the current date and the 2 preceding days of data (using ROWS BETWEEN 2 PRECEDING AND CURRENT ROW on the aggregated daily data).
4. Exports the results to a CSV file at `/home/user/report.csv` with the following columns exactly in this order:
   `base_product_id`, `accessory_product_id`, `sale_date`, `daily_total`, `rolling_3d_avg`
   Sort the final output by `base_product_id` ASC, `accessory_product_id` ASC, and `sale_date` ASC.
   Round the `rolling_3d_avg` to 2 decimal places.

Make sure your script creates the output CSV file correctly, including the header row. You can use the built-in `sqlite3` and `csv` modules in Python. Run your script to generate the output file.