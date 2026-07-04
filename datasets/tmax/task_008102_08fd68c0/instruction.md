You are a database administrator tasked with analyzing user behavior in an e-commerce platform. The system's data is stored in a SQLite database representing a bipartite graph of users and products, along with their interactions.

The database is located at `/home/user/ecommerce_graph.db` and contains the following tables:
- `users`: `id` (INTEGER PRIMARY KEY), `name` (TEXT), `is_active` (INTEGER)
- `products`: `id` (INTEGER PRIMARY KEY), `name` (TEXT), `category` (TEXT), `price` (REAL)
- `views`: `user_id` (INTEGER), `product_id` (INTEGER), `view_date` (TEXT)
- `purchases`: `user_id` (INTEGER), `product_id` (INTEGER), `purchase_date` (TEXT)

Your objective is to identify trends among a specific segment of users. You must find the **top 5 most frequently purchased product categories** by users who meet ALL of the following criteria:
1. The user is currently active (`is_active = 1`).
2. The user has viewed at least one product in the `'Electronics'` category.
3. The user has NEVER purchased any product in the `'Electronics'` category.

For these specific target users, calculate the total number of purchases they have made in each product category. 
Order the results primarily by the purchase count in descending order. If there is a tie in the purchase count, sort those tied categories alphabetically by category name in ascending order. Limit the final output to the top 5 categories.

You must export your final results into a JSON file located at `/home/user/solution.json`. The file should contain a single JSON array of objects, where each object has exactly two keys: `"category"` (string) and `"purchase_count"` (integer).

Example expected output format:
```json
[
  {"category": "Clothing", "purchase_count": 45},
  {"category": "Home", "purchase_count": 32},
  {"category": "Books", "purchase_count": 12}
]
```

You may use any language or tool available in your environment (e.g., Python, Bash, sqlite3 CLI) to map the relationships, run the query, and format the export.