You are acting as a Database Administrator for a growing e-commerce startup. Recently, concurrent transactions processing pending orders have been experiencing severe performance degradation and occasional database locks due to full table scans. 

You have been given a copy of the production SQLite database located at `/home/user/store.db`. Your task is to resolve the performance issue by designing the correct index, and then build a data export pipeline to feed an external NoSQL document store.

Specifically, you need to:

1. **Analyze and Optimize:**
   Identify the tables in `/home/user/store.db`. The application frequently runs a query to fetch orders where `status = 'pending'`, sorted by `created_at` in descending order. 
   Create a composite index named `idx_orders_status_date` on the `orders` table to optimize this specific access pattern (filtering by status and sorting by creation date). 

2. **Verify the Optimization:**
   Generate the `EXPLAIN QUERY PLAN` for the query: 
   `SELECT orders.id, customers.name, customers.email, orders.total, orders.created_at FROM orders JOIN customers ON orders.customer_id = customers.id WHERE orders.status = 'pending' ORDER BY orders.created_at DESC LIMIT 20;`
   Save the exact output of this `EXPLAIN QUERY PLAN` command to `/home/user/plan.txt`.

3. **Data Export & Representation Mapping:**
   Using Python, write a script `/home/user/export_pending.py` that executes the optimized query above (fetching the top 20 pending orders).
   The script must format the relational result into a Document-style JSON array and export it to `/home/user/top_pending.json`.
   Each JSON object in the array must strictly have the following keys:
   - `order_id` (integer)
   - `customer_name` (string)
   - `customer_email` (string)
   - `order_total` (float)
   - `order_date` (string)

Ensure your Python script runs successfully and generates the `/home/user/top_pending.json` file. All files should be placed in `/home/user/`.