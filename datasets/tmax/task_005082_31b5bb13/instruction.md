You are a data analyst working with e-commerce transaction logs. You have been given a CSV file containing transaction records at `/home/user/data/transactions.csv`. The file has the following columns: `id,timestamp,category,price,user_id`.

Your task is to write a Python script at `/home/user/process_data.py` that processes this data using an in-memory SQLite database. The script must fulfill the following requirements:

1. **CLI Arguments**: The script must use `argparse` to accept the following arguments:
   - `--category` (string): The product category to filter by.
   - `--min_price` (float): The minimum price (inclusive) to filter by.
   - `--page` (int): The 1-indexed page number for pagination.
   - `--page_size` (int): The number of records per page.

2. **Database Operations**:
   - Read the CSV file into an in-memory SQLite database (`sqlite3.connect(':memory:')`).
   - Create a table named `transactions` with appropriate data types (`id` INTEGER, `timestamp` TEXT, `category` TEXT, `price` REAL, `user_id` INTEGER).
   - Create a composite index named `idx_category_price` on the `category` and `price` columns to optimize the filtering strategy.

3. **Query Execution**:
   - Write a **parameterized SQL query** to prevent SQL injection.
   - Filter the records by exact `category` match and `price >= min_price`.
   - Sort the results by `price` in descending order. If prices are equal, sort by `id` in ascending order.
   - Paginate the results using the provided `--page` and `--page_size` arguments (e.g., page 1 with size 10 returns rows 1-10, page 2 returns 11-20).

4. **Output**:
   - Write the resulting rows to a CSV file at `/home/user/output.csv`.
   - The output CSV must include the header row (`id,timestamp,category,price,user_id`) followed by the data rows for the requested page.

After writing the script, execute it with the following command to generate the output file:
`python3 /home/user/process_data.py --category electronics --min_price 150.0 --page 2 --page_size 2`