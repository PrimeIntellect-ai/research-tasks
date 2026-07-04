You are a Database Administrator and Data Engineer. We have an undocumented SQLite database at `/home/user/logistics.db` containing e-commerce data. Previously, our system extracted all rows into memory and used slow Pandas aggregations to generate our VIP customer report. Your task is to reverse-engineer the database schema, push the computation down to the database layer using advanced SQL (CTEs, Window Functions, and Joins), and output a hierarchical JSON document.

Write a Python script at `/home/user/optimize_pipeline.py` that connects to `/home/user/logistics.db` and generates a report saved to `/home/user/top_customers_report.json`.

The report must follow these exact business rules:
1. Identify the top 5 customers globally based on their total lifetime spend (quantity * unit_price across all their orders).
2. For each of these 5 customers, calculate their overall `spend_rank` among ALL customers in the database (e.g., the top spender is rank 1). Use SQL Window functions for this.
3. For each of these 5 customers, identify the top 3 product categories they spent the most money on.
4. Output a cross-representation mapping (relational to document) in the form of a JSON array of objects.

The output JSON in `/home/user/top_customers_report.json` must exactly match this structure:
```json
[
  {
    "customer_id": 10,
    "customer_name": "Alice Smith",
    "segment": "Enterprise",
    "lifetime_spend": 15430.50,
    "spend_rank": 1,
    "top_categories": [
      {
        "category_name": "Electronics",
        "category_spend": 10000.00
      },
      ... up to 3 categories
    ]
  },
  ... 4 more customers
]
```

Requirements:
- Ensure all monetary amounts (like `lifetime_spend` and `category_spend`) are rounded to 2 decimal places.
- The top-level array should be sorted by `spend_rank` ascending (1 to 5).
- The `top_categories` array must be sorted by `category_spend` descending.
- Do not use ORMs like SQLAlchemy; use the standard `sqlite3` Python library to execute your optimized SQL. You can execute one large query or a few chained queries, but do not fetch raw table dumps into Python.