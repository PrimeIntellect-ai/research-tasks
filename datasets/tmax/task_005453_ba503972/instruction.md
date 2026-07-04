You are a data engineer tasked with migrating data from a legacy relational format into a document-oriented NoSQL format (MongoDB), and designing the subsequent analytical queries. 

There are three CSV files located in `/home/user/data/`:
1. `users.csv`: `user_id,name`
2. `orders.csv`: `order_id,user_id,order_date,status`
3. `order_items.csv`: `item_id,order_id,product_name,price`

Your objective is to write a Python script at `/home/user/process_etl.py` that performs the following tasks:

**1. Cross-representation Mapping (Relational to Document)**
Read the CSV files and map the relational data into a nested document format. Create a JSON array of "user" documents and save it to `/home/user/output/documents.json`. 
Each user document must have the following exact structure:
```json
{
  "user_id": "1",
  "name": "Alice",
  "orders": [
    {
      "order_id": "101",
      "order_date": "2023-01-15",
      "status": "completed",
      "items": [
        {
          "item_id": "501",
          "product_name": "Widget A",
          "price": 25.50
        }
      ]
    }
  ]
}
```
*Ensure all numeric fields (like price) are represented as floats, and strings as strings. Omit empty arrays if a user has no orders, or an order has no items.*

**2. NoSQL Aggregation Pipeline Design**
Design a MongoDB aggregation pipeline (as a JSON array of pipeline stages) that processes the `users` collection (matching the structure you just created) to find the top 5 users (returning `user_id`, `name`, and `total_widget_spent`) based on the total money spent specifically on items where `product_name` contains the word "Widget", but ONLY considering orders where `status` is "completed". 
Save this pipeline array to `/home/user/output/pipeline.json`. 
*(Note: Use standard MongoDB aggregation operators like `$match`, `$unwind`, `$group`, `$sort`, `$limit`).*

**3. Index Strategy Design**
To prevent a scenario where this query requires a full collection scan (which previously caused query deadlocks on our production system under heavy load), design the optimal index or indexes for this query. 
Save your index definitions as a JSON list of objects to `/home/user/output/indexes.json`. Each object should represent one index in the format expected by PyMongo's `create_index`, for example:
```json
[
  {
    "keys": [("field1", 1), ("field2", -1)],
    "unique": false
  }
]
```
*(Hint: Think about which fields are used for filtering before unwinding).*

Your Python script `/home/user/process_etl.py` should generate these three files when run. Do not start a MongoDB server; we are purely evaluating the ETL mapping and pipeline/index design artifacts.