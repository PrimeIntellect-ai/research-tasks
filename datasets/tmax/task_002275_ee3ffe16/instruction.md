You are a data engineer tasked with building an ETL pipeline that transforms relational e-commerce data into a knowledge graph representation to extract complex patterns. 

You have been provided with a SQLite database at `/home/user/ecommerce.db` containing four tables:
1. `users` (id, name)
2. `products` (id, title, category)
3. `purchases` (id, user_id, product_id, purchase_date)
4. `reviews` (id, user_id, product_id, rating, review_text)

Your objective is to write and execute a Python script (`/home/user/run_pipeline.py`) that performs the following:

**Phase 1: Relational to Graph ETL**
Extract the data and build an in-memory knowledge graph (using `networkx` or your own data structures). The graph must contain two types of nodes (`User` and `Product`) and two types of directed edges:
- `PURCHASED`: from User to Product (derived from the `purchases` table).
- `REVIEWED`: from User to Product, containing the `rating` as an edge attribute (derived from the `reviews` table).
*Requirement:* You must use parameterized SQL queries when reading the relational data to prevent SQL injection, even though this is an internal database.

**Phase 2: Knowledge Graph Pattern Matching**
Search the graph to find a specific pattern: "Products that share buyers with poorly reviewed products".
Specifically, find all distinct `Product` nodes (let's call them "Target Products") that satisfy the following conditions:
1. A User `U` purchased Product `A`.
2. User `U` left a `1` star review for Product `A` (rating = 1).
3. The same User `U` also purchased a different Product `B` (the Target Product).
4. Product `B` is NOT Product `A`.

**Phase 3: Result Processing**
For all Target Products (`Product B`) identified in Phase 2, aggregate them by category. 
Write the results to `/home/user/insights.json` as a JSON object where the keys are the `category` strings, and the values are sorted lists of `title` strings for the Target Products in that category. 

Example format for `/home/user/insights.json`:
```json
{
  "Electronics": ["Bluetooth Speaker", "Wireless Mouse"],
  "Books": ["Python for Data Analysis"]
}
```

Ensure the script can be run using `python3 /home/user/run_pipeline.py`. If you need to install any packages like `networkx`, you may use `pip`.