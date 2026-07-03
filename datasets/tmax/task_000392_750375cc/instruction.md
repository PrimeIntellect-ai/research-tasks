You are a data engineer tasked with building a highly efficient API to serve complex queries from an SQLite database for an ETL monitoring dashboard.

We have an e-commerce database located at `/home/user/ecommerce.db` containing the following tables:
- `customers` (id, name, email)
- `products` (id, name, category, price)
- `orders` (id, customer_id, order_date)
- `order_items` (id, order_id, product_id, quantity)

Your tasks:
1. **Fix the Vendored Web Framework**: We are using a minimalist, internally developed web framework located at `/app/vendored_microframe/`. It has a known bug where it fails to parse standard URL query parameters (it was accidentally modified to split on semicolons instead of ampersands). Find and fix this bug so it properly parses `&`-separated query string arguments.
2. **Implement the API Endpoint**: Create a server script in your language of choice that imports or uses the fixed framework and listens on `127.0.0.1:8080`.
   - Implement a GET endpoint at `/api/top_customers`.
   - It must accept two query parameters: `category` (string) and `limit` (integer).
   - The endpoint must execute a parameterized SQL query to find the top customers by total spend strictly for products in the specified `category`. The returned JSON should be a list of objects with the keys `customer_name` and `total_spend` (rounded to 2 decimal places), ordered by `total_spend` descending.
3. **Database Optimization**: Analyze your query's execution plan. The current schema has no indexes (other than primary keys). You must create at least two indexes in `/home/user/ecommerce.db` named `idx_product_category` (on `products.category`) and `idx_order_items_product` (on `order_items.product_id`) to optimize the joins and filtering, ensuring the query plan does not require full table scans on these columns.

Keep the server running in the background or foreground so it can be queried. Create a file `/home/user/server_ready` with the word "READY" once your server is up and listening.