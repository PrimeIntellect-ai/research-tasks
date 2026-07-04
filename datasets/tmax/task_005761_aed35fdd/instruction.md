You are a data engineer building ETL pipelines. Your team is migrating a legacy e-commerce application. You need to analyze the database schema, map the relationships as a knowledge graph to understand data lineage, and design an indexing strategy for a heavy ETL query.

An SQLite database has been provided at `/home/user/ecommerce.db`.

**Part 1: Schema Analysis & Knowledge Graph Pattern Matching**
You must write a Python script `/home/user/etl_schema_graph.py` that reads the schema of `/home/user/ecommerce.db`. 
Treat the schema as a directed graph where tables are nodes, and foreign keys are directed edges. A directed edge goes from the table *containing* the foreign key to the table being *referenced* (e.g., if `orders` has a `user_id` referencing `users`, the edge is `orders` -> `users`).

Your script must traverse this graph to find all tables that are exactly 1 hop and exactly 2 hops away from the `users` table (i.e., tables that reference `users` directly, and tables that reference tables that reference `users`).
The script should output the results to `/home/user/schema_hops.json` in the following exact JSON format (lists must be sorted alphabetically):
```json
{
  "1_hop": ["table_a", "table_b"],
  "2_hops": ["table_c", "table_d"]
}
```

**Part 2: Index Strategy Design**
A daily ETL job runs the following heavy query:
```sql
SELECT u.email, sum(oi.quantity * p.price) 
FROM users u 
JOIN orders o ON u.id = o.user_id 
JOIN order_items oi ON o.id = oi.order_id 
JOIN products p ON oi.product_id = p.id 
WHERE o.status = 'COMPLETED' AND o.created_at >= '2023-01-01' 
GROUP BY u.email;
```
Write a single SQL file at `/home/user/optimize.sql` containing exactly one `CREATE INDEX` statement named `idx_orders_etl` on the `orders` table. This index must be designed to optimally speed up the filtering (`status`, `created_at`) and the subsequent join (`user_id`) for this specific query. Order the columns in the index based on standard indexing best practices (equality filters first, then range filters/join keys).

Complete both parts to finish the task.