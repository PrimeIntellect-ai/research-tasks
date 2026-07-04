You are a Database Reliability Engineer managing the backup infrastructure for a small e-commerce application. 

The current backup script pulls data from an SQLite database (`/home/user/ecommerce.db`), but it causes `database is locked` errors in production because it uses highly inefficient N+1 queries. It holds a read lock for an extended period, which eventually deadlocks with concurrent background writes. 

Your task is to replace this process by writing a single, highly optimized SQL query to extract the required backup data, and then export it to a specific JSON format using Python. 

The database schema contains three tables:
- `customers` (id, name, email)
- `orders` (id, customer_id, order_date, status)
- `items` (id, order_id, product_name, price)

Requirements for the backup:
1. You must export data ONLY for customers who have at least one order with the status `'completed'`.
2. Only include `'completed'` orders in the output. Ignore orders with any other status (and their items).
3. Write a Python script `/home/user/export_backup.py` that connects to `/home/user/ecommerce.db`, executes **exactly one SQL query** to fetch all necessary data, and writes the output to `/home/user/backup_data.json`.
4. The output `/home/user/backup_data.json` must be a meticulously formatted JSON array of customer objects. Each customer object must include a calculated `total_spent` (the sum of the prices of all items across all their *completed* orders).

The required JSON structure is as follows:
```json
[
  {
    "customer_id": 1,
    "name": "Alice Smith",
    "email": "alice@example.com",
    "total_spent": 150.50,
    "orders": [
      {
        "order_id": 101,
        "order_date": "2023-10-01",
        "items": [
          {
            "product_name": "Wireless Mouse",
            "price": 25.50
          },
          {
            "product_name": "Mechanical Keyboard",
            "price": 125.00
          }
        ]
      }
    ]
  }
]
```
Note: Ensure that the JSON is properly formatted and indented (2 spaces). Customers should be sorted by `customer_id` ascending. Inside each customer, `orders` should be sorted by `order_id` ascending. Inside each order, `items` should be sorted by `product_name` alphabetically ascending. `total_spent` must be a float.

Do not modify the database. Only read from it and generate the `backup_data.json` file.