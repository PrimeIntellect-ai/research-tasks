You are a Data Engineer building an ETL pipeline that transforms relational e-commerce data into a graph structure for recommendation analysis. 

A SQLite database is located at `/home/user/ecommerce.db`. It contains three tables:
1. `users` (`user_id` INTEGER, `name` TEXT)
2. `products` (`product_id` INTEGER, `category` TEXT)
3. `purchases` (`user_id` INTEGER, `product_id` INTEGER, `purchase_date` TEXT)

Your task is to write a Python script `/home/user/etl_graph.py` that performs the following steps:
1. **Parameterized Extraction**: Query the database to extract all purchases where the product's `category` is exactly `'Electronics'` and the `purchase_date` is on or after `'2023-01-01'`. You must use parameterized SQL queries (do not use string formatting for the parameters).
2. **Schema Mapping & Bipartite Graph**: Map the extracted relational data into an in-memory bipartite graph using the `networkx` library, where nodes are users and products, and edges are purchases.
3. **Graph Projection**: Project this bipartite graph into a User-to-User unipartite graph. An edge should exist between two users if they purchased the *same* electronics product. The `weight` of the edge between User A and User B must be the total number of distinct products they both purchased. Do not include self-loops (edges from a user to themselves).
4. **Materialization**: Find the top 3 user pairs with the highest edge weights. If there is a tie in weights, order them by User A's ID ascending, then User B's ID ascending (where User A's ID < User B's ID). 
5. Write this top 3 result to a JSON file at `/home/user/top_user_pairs.json` in the following exact format:
```json
[
  {"user_a": 1, "user_b": 2, "weight": 4},
  {"user_a": 3, "user_b": 5, "weight": 2},
  {"user_a": 2, "user_b": 7, "weight": 2}
]
```

Requirements:
- Ensure `/home/user/top_user_pairs.json` is created upon running `python3 /home/user/etl_graph.py`.
- Ensure the user pairs in the output always have `user_a` < `user_b`.
- Use the `networkx` library for graph operations. You may install it if it is not present.