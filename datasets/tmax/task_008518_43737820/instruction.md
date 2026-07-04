You are a data engineer tasked with building a lightweight ETL pipeline using Python. 

We have exported raw data from our legacy document database into two JSON Lines files located at:
1. `/home/user/data/users.jsonl`
2. `/home/user/data/orders.jsonl`

The data model is poorly documented and heterogeneous (requiring reverse engineering and schema analysis). 
- The `users.jsonl` file contains basic user profiles.
- The `orders.jsonl` file contains order documents. An order contains an array of `items`. However, because of legacy systems, an item can either be a standard item object, or an array of item objects (representing a bundle). 
- Furthermore, pricing is inconsistent: prices might be stored as an integer in cents (e.g., `price_cents: 1250`), a float (e.g., `price: 12.50`), or a string with a dollar sign (e.g., `cost: "$12.50"`).
- Items also have a `category` field.

Your task is to write a Python script at `/home/user/etl_pipeline.py` that performs the equivalent of a NoSQL aggregation pipeline:
1. Load and parse the users and orders.
2. Join the orders to the users based on the appropriate ID fields (you will need to inspect the files to map the relationship).
3. "Unwind" the items in each order (flattening any bundles so they are treated as individual items).
4. Standardize all item prices into a standard USD float value.
5. Aggregate the data per user to calculate:
   - `total_spent`: The sum of all item prices across all orders for that user (rounded to 2 decimal places).
   - `order_count`: The total number of distinct orders placed by the user.
   - `top_category`: The category from which the user bought the highest quantity of items. If there is a tie, pick the one that comes first alphabetically.

Your script must execute and output the final aggregated data to `/home/user/user_spend.jsonl`. 
The output must strictly conform to the following JSON Lines schema for each line:
`{"user_id": "<string>", "email": "<string>", "total_spent": <float>, "order_count": <int>, "top_category": "<string>"}`

The output file must be sorted alphabetically by `user_id`.

Please investigate the data files, write the pipeline script, and run it to produce the final `/home/user/user_spend.jsonl` file.