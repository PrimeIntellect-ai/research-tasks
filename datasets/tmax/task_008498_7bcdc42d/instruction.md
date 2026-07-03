You are acting as a Database Administrator and Data Engineer. 

We have a Python script at `/home/user/generate_report.py` that queries a SQLite database (`/home/user/ecommerce.db`) to generate a revenue report. However, the report is currently outputting astronomically high and incorrect revenue numbers. We suspect there is an implicit cross join in the SQL query.

The database has the following schema:
- `customers` (`id`, `name`, `region`)
- `orders` (`id`, `customer_id`, `order_date`)
- `order_items` (`id`, `order_id`, `product_id`, `quantity`, `price`)
- `products` (`id`, `name`, `category`)

Your task:
1. Fix the SQL query in `/home/user/generate_report.py` so that it correctly calculates the `total_revenue` (`quantity * price`) per `customer_name` and `product_category` for customers in the 'North America' region. 
2. Ensure you use proper explicit joins to prevent any cross-product explosion.
3. Modify the Python script to build a data pipeline that processes the fetched database results:
   - Filter out any rows where `total_revenue` is strictly less than or equal to 100.
   - Sort the remaining results primarily by `total_revenue` descending, and secondarily by `customer_name` ascending.
   - Implement pagination: extract exactly Page 2, where each page contains exactly 2 items (i.e., skip the first 2 results, and return the next 2).
4. Save the final paginated results as a JSON array to `/home/user/final_report.json`. 

Each object in the JSON array must exactly match this structure:
```json
[
  {
    "customer_name": "Alice",
    "product_category": "Electronics",
    "total_revenue": 250.50
  }
]
```

Do not modify the database schema or data. Only fix the script and output the `final_report.json`.