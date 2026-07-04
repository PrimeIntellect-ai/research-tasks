You are a Database Administrator tasked with optimizing and extracting an analytical report from a poorly performing e-commerce SQLite database. 

The database is located at `/home/user/ecommerce.db` and has the following schema:
- `customers` (`id` INTEGER PRIMARY KEY, `joined_date` TEXT, `country` TEXT)
- `orders` (`id` INTEGER PRIMARY KEY, `customer_id` INTEGER, `order_date` TEXT, `total_amount` REAL)
- `order_items` (`id` INTEGER PRIMARY KEY, `order_id` INTEGER, `product_id` INTEGER, `quantity` INTEGER, `price` REAL)
- `products` (`id` INTEGER PRIMARY KEY, `category` TEXT, `name` TEXT)

Your goal is to write a Python script at `/home/user/optimize_and_export.py` that performs the following tasks:
1. **Optimize:** Add necessary SQL indexes to the database to speed up joins between these tables (specifically targeting foreign keys and date columns).
2. **Query Pipeline & Aggregation:** Construct and execute a query pipeline (using CTEs or temporary tables) to aggregate customer data into monthly cohorts. A cohort is defined by the `YYYY-MM` of the customer's `joined_date`.
3. **Summarization:** For each cohort, calculate:
   - `total_clv`: The sum of `total_amount` from all orders placed by customers in that cohort.
   - `top_categories`: The top 2 product categories by total revenue (calculated as `quantity * price` from `order_items`) purchased by customers in that cohort.
4. **Export:** Format the aggregated results and export them directly to a gzip-compressed JSON Lines file at `/home/user/cohort_report.jsonl.gz`.

Each line in the exported `.jsonl.gz` file must be a valid JSON object matching this exact structure:
```json
{
  "cohort": "2023-01",
  "total_clv": 15430.50,
  "top_categories": [
    {"category": "Electronics", "revenue": 8500.00},
    {"category": "Apparel", "revenue": 4200.00}
  ]
}
```
*Note: Sort the output JSON lines ascending by the `cohort` string. Round all floating-point numbers to 2 decimal places.*

Execute your script to produce the output file. Ensure all necessary Python packages are installed (standard library modules like `sqlite3`, `json`, and `gzip` are sufficient).