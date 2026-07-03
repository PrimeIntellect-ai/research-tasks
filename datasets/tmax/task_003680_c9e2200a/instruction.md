You are acting as a Database Administrator tasked with migrating data from a legacy relational database to a document database to optimize our analytics queries.

We have an SQLite database located at `/home/user/sales.db` with the following schema:
- `customers` (id INTEGER PRIMARY KEY, name TEXT, region TEXT)
- `orders` (id INTEGER PRIMARY KEY, customer_id INTEGER, order_date TEXT)
- `items` (id INTEGER PRIMARY KEY, order_id INTEGER, product TEXT, price REAL, quantity INTEGER)

Your task is to:
1. Ensure a MongoDB server is running locally on the default port (27017). You may need to start the service or run it in the background if it's installed but not running.
2. Write and execute a Python script (`/home/user/migrate.py`) using `sqlite3` and `pymongo` (you may need to install `pymongo`) that reads all data from `/home/user/sales.db` and loads it into a MongoDB database named `analytics`, in a collection named `customer_orders`.
3. The MongoDB documents should be structured hierarchically. Each document must represent one customer and contain an array of their orders, where each order contains an array of its items. 
   Document structure example:
   ```json
   {
     "_id": 1,
     "name": "Alice",
     "region": "North",
     "orders": [
       {
         "order_id": 101,
         "order_date": "2023-01-15",
         "items": [
           {"product": "Widget", "price": 10.5, "quantity": 2}
         ]
       }
     ]
   }
   ```
4. After migrating the data, your script must execute a MongoDB aggregation pipeline on the `customer_orders` collection to find the top 3 customers by total amount spent (price * quantity across all items in all orders).
5. The script must output the result of this aggregation to a JSON file at `/home/user/top_customers.json`.
   The output must be a valid JSON array of objects, strictly matching this format:
   ```json
   [
     {"name": "Customer Name", "region": "Region Name", "total_spent": 150.0},
     ...
   ]
   ```
   Sort the array in descending order of `total_spent`. If there is a tie, sort alphabetically by `name`.

Complete the data migration and generate the `/home/user/top_customers.json` file.