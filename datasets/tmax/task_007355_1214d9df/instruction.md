You are a data engineer tasked with building a mini ETL pipeline to migrate nested document-style data into a normalized relational database, and then building a reporting query on top of it. 

I have a raw data file located at `/home/user/raw_data/orders.json` containing e-commerce orders in a nested JSON format (document representation). 

Your task consists of two parts:

**Part 1: ETL Pipeline (Document to Relational Mapping)**
Write a Python script at `/home/user/etl.py` that reads `/home/user/raw_data/orders.json` and loads it into a normalized SQLite database at `/home/user/ecommerce.db`. 
You must reverse-engineer the JSON structure and map it to exactly these four tables with the specified schemas:
1. `users` (`user_id` TEXT PRIMARY KEY, `name` TEXT, `email` TEXT)
2. `products` (`product_id` TEXT PRIMARY KEY, `name` TEXT, `category` TEXT, `price` REAL)
3. `orders` (`order_id` TEXT PRIMARY KEY, `user_id` TEXT, `order_date` TEXT)
4. `order_items` (`order_id` TEXT, `product_id` TEXT, `quantity` INTEGER)
*(Note: Deduplicate users and products. If a product or user appears multiple times with the same ID, just insert it once).*

**Part 2: Query and Schema Validation**
Write a second Python script at `/home/user/report.py` that connects to `/home/user/ecommerce.db` and generates a summary report.
The report must identify the top spending user for *each* product category.
The calculation for spending is `price * quantity`.
If there is a tie for the highest spender in a category, resolve it by selecting the user with the lexicographically smallest `name`.

Your script must execute this query and output the results as a JSON array to `/home/user/summary.json`.
The output JSON must strictly validate against this structure/schema:
```json
[
  {
    "category": "Electronics",
    "top_user_name": "Alice Smith",
    "total_spent_by_top_user": 1200.50
  },
  ...
]
```
The array must be sorted alphabetically by `category`. Ensure the `total_spent_by_top_user` is a float, rounded to 2 decimal places.

Run both of your scripts so that `/home/user/ecommerce.db` and `/home/user/summary.json` are fully generated and populated.