You are a data engineer building an ETL pipeline that combines NoSQL-style data extraction with knowledge graph pattern matching. 

You have been provided with a SQLite database at `/home/user/data_lake.db` containing a single table: `documents(id INTEGER PRIMARY KEY, doc TEXT)`. The `doc` column contains JSON strings representing different entities in a NoSQL-like document structure. 

The documents have a `type` field which can be `"user"`, `"product"`, or `"purchase"`. 
A purchase document looks like this: `{"type": "purchase", "user_id": "U123", "product_id": "P456", "timestamp": 1670000000}`.

Your task is to:
1. **Index Strategy**: Analyze the JSON schema and write a SQL script at `/home/user/optimize.sql` that creates a covering index (or an index on extracted JSON expressions) to optimize the retrieval of `user_id` and `product_id` specifically for documents where `type = 'purchase'`.
2. **Pipeline Chaining & Graph Matching**: Write a Python script at `/home/user/pipeline.py` that:
   - Connects to `/home/user/data_lake.db`.
   - Extracts all user-product purchase relationships.
   - Builds a bipartite graph (Users and Products) to perform pattern matching.
   - Finds all pairs of unique users `(UserA, UserB)` who have purchased **exactly 3** of the exact same products. 
   - To avoid duplicates, ensure `UserA < UserB` (lexicographically).
3. **Output**: Your Python script must output the resulting user pairs to a text file at `/home/user/matching_users.txt`. 
   - Each line must contain a comma-separated pair: `UserA,UserB`.
   - The lines must be sorted alphabetically.

Do not use absolute paths to Python executables, assume `python3` is available. You may install standard data processing libraries like `networkx` via pip if you wish.