You are a Data Engineer building a custom ETL pipeline to migrate an undocumented legacy system to a new Knowledge Graph analytics platform.

An unknown legacy SQLite database has been provided to you at `/home/user/data.db`. You do not know the schema, but you know it contains information about customers, items, purchases (transactions), and reviews (feedback).

Your task has three parts:

1. **Reverse Engineer & Extract**: Inspect `/home/user/data.db` to understand its schema. Write a Python script `/home/user/etl.py` that connects to this database and exports the relational data into a graph document format. 
   - Create a directory `/home/user/graph/`.
   - The script must generate `/home/user/graph/nodes.jsonl` and `/home/user/graph/edges.jsonl`.
   - **Nodes**: Must have the format `{"id": "<prefix_id>", "type": "<type>", "properties": {<all_other_columns>}}`. Prefix customer IDs with `c_` (e.g., `c_1`) and set type to `customer`. Prefix item IDs with `i_` (e.g., `i_101`) and set type to `item`.
   - **Edges**: Must have the format `{"src": "<node_id>", "dst": "<node_id>", "type": "<type>", "properties": {<all_other_columns_except_ids>}}`. Transactions should become `PURCHASED` edges from a customer to an item. Feedbacks/reviews should become `RATED` edges from a customer to an item.

2. **Cross-Representation Pipeline**: Chain this data into a new analytical script. Write a second Python script `/home/user/query.py` that reads the two JSONL files created in Step 1 (do NOT connect to the SQLite DB in this script) and performs an in-memory graph pattern match.

3. **Graph Pattern Matching**: The analytics team needs to identify a very specific cohort of customers. Have `/home/user/query.py` find all customers (Customer A) who meet ALL of the following conditions:
   - Customer A `PURCHASED` an Item X.
   - A *different* customer (Customer B) `RATED` that same Item X with a `rating` of 5.
   - Customer A ALSO `RATED` some Item Y (which can be any item) with a `rating` of 1.

The output of `/home/user/query.py` must write the names of the matching customers (one name per line, sorted alphabetically) to `/home/user/target_customers.txt`.

Execute your scripts to generate the final files. You can use any standard tools available in the Linux environment.