You are a data analyst tasked with processing e-commerce CSV files. You have two files:
1. `/home/user/products.csv` containing product catalog information.
2. `/home/user/transactions.csv` containing raw sales data.

Your goal is to write and execute a Python script located at `/home/user/process_sales.py` that processes these files and produces a cleaned, joined, and validated JSON Lines (JSONL) file at `/home/user/high_value_active_sales.jsonl`.

Requirements for `/home/user/process_sales.py`:
1. **Index Strategy:** Read `products.csv` and build an efficient in-memory index (e.g., a dictionary) keyed by `product_id` to allow O(1) lookups. Do not load all transactions into memory at once.
2. **Query-to-Pipeline:** Stream `transactions.csv` row by row. For each transaction, look up the product in your index.
3. **Filtering:** Keep only transactions where the product's `is_active` status is strictly `'true'` and the transaction `amount` is strictly greater than `100.0`.
4. **Schema Validation:** Ensure the resulting output matches the following exact JSON schema structure for each line:
   - `transaction_id` (string): The `tx_id` from transactions.
   - `user` (string): The `user_id` from transactions.
   - `category` (string): The `category` from products.
   - `total_value` (float): The `amount` from transactions, cast to a float.

Input file schemas:
- `products.csv`: `product_id,category,price,is_active`
- `transactions.csv`: `tx_id,product_id,user_id,amount,timestamp`

Write the Python script, run it, and ensure `/home/user/high_value_active_sales.jsonl` is created with the correctly processed data.