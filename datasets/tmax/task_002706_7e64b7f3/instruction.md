You are tasked with building a cross-database analytics tool for processing e-commerce CSV files. The system uses PostgreSQL for relational transactional data and MongoDB for product relationship graph data.

**Environment & Setup:**
1. Execute `/app/start_services.sh` to start PostgreSQL (port 5432) and MongoDB (port 27017).
2. The PostgreSQL credentials are user: `analyst`, password: `data`, database: `store`.
3. The MongoDB instance has no auth required. Use the database name `store`.

**Data Ingestion:**
You have four CSV files located in `/app/data/`:
* `users.csv` (id, name, signup_date)
* `purchases.csv` (id, user_id, product_id, amount_cents)
* `products.csv` (id, name, category)
* `product_edges.csv` (source_product_id, target_product_id, similarity_score) - *Similarity scores are floats.*

You must create appropriate schemas and load `users.csv` and `purchases.csv` into PostgreSQL. 
You must load `products.csv` and `product_edges.csv` into MongoDB (collections: `products`, `edges`).

**Go Application:**
Write a Go program located exactly at `/home/user/query_tool`. 
The program must read a JSON array of integer `user_id`s from `stdin` (e.g., `[1, 5, 12]`).

For each `user_id` provided, the program must compute:
1. `total_spent_cents`: The sum of all purchase amounts for this user (from PostgreSQL). If the user has no purchases, this is 0.
2. `top_category`: The product category the user has bought the most items from. You will need to join PostgreSQL purchases with MongoDB product data to determine this. If there is a tie, pick the category name that comes first alphabetically. If no purchases, return `""`.
3. `recommended_product_ids`: A 1-hop graph projection. Find all products the user has purchased. Then, find all `target_product_id`s connected to those purchased products in MongoDB where the `similarity_score` is `>= 0.80`. Return a deduplicated list of these recommended product IDs, sorted in ascending numerical order. Exclude products the user has already purchased.

**Output Format:**
The program must output a strictly formatted JSON array of objects to `stdout`. The array must be sorted by `user_id` ascending.
Example output:
```json
[
  {
    "user_id": 1,
    "total_spent_cents": 15000,
    "top_category": "Electronics",
    "recommended_product_ids": [105, 203, 408]
  },
  {
    "user_id": 5,
    "total_spent_cents": 0,
    "top_category": "",
    "recommended_product_ids": []
  }
]
```

Your program must compile to a binary executable at `/home/user/query_tool`. Make sure to install any required Go drivers (e.g., `pgx`, `mongo-driver`) using `go get` in a Go module initialized in `/home/user/`.