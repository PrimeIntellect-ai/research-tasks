You are acting as a data analyst. I have three CSV files containing e-commerce data in `/home/user/data/`:
1. `customers.csv`: `customer_id`, `name`, `segment`
2. `products.csv`: `product_id`, `name`, `category`, `price`
3. `transactions.csv`: `transaction_id`, `customer_id`, `product_id`, `transaction_date`, `quantity`

Your task is to process this data using SQLite and Bash. Complete the following steps:

1. Create a SQLite database at `/home/user/ecommerce.db`.
2. Import the three CSV files into tables named `customers`, `products`, and `transactions` respectively. Infer the schema appropriately.
3. Analyze the schema relationships and create the following indexes to optimize query performance:
   - An index named `idx_transactions_date` on the `transaction_date` column in `transactions`.
   - An index named `idx_products_category` on the `category` column in `products`.
   - An index named `idx_transactions_customer` on the `customer_id` column in `transactions`.
4. Write a Bash script at `/home/user/analyze.sh` that executes a SQL query against `/home/user/ecommerce.db` to calculate the total revenue (sum of `quantity * price`) per customer `segment` for the product category `'Electronics'` for transactions that occurred in the year `2023` (dates between `2023-01-01` and `2023-12-31`).
5. The Bash script must output the result in JSON format and save it to `/home/user/report.json`. The JSON should be an array of objects, each containing the keys `"segment"` and `"total_revenue"`, sorted by `"total_revenue"` in descending order.

Make sure `/home/user/analyze.sh` is executable and runs successfully without any arguments, producing the exact file `/home/user/report.json`. Use `sqlite3` for database operations.