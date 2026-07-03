You are a data engineer building an ETL pipeline to extract supply chain patterns from an internal knowledge graph. 

A raw, unindexed SQLite database containing the graph data will be located at `/home/user/graph.db`. 

The database has the following schema:
- Table `nodes`: `id` (TEXT), `label` (TEXT)
- Table `edges`: `source` (TEXT), `target` (TEXT), `cost` (REAL)

Your task is to process this graph data and extract optimal routing information. Follow these steps carefully:

1. **Index Strategy Design**: The database currently has no indexes. To optimize your downstream queries, determine the best columns to index for fast graph traversal and label filtering. Write your SQL `CREATE INDEX` statements into a file named `/home/user/indexes.sql`, and execute them against `/home/user/graph.db`.

2. **Knowledge Graph Pattern Matching**: Write a Python script at `/home/user/etl_pipeline.py`. Using the standard `sqlite3` library, query the database to find all valid "Supply Chains". A valid supply chain is defined as a sequence of exactly 3 nodes and 2 edges: 
   `Supplier` (node) -> `Manufacturer` (node) -> `Retailer` (node). 
   The direction of the edges must match this flow (source -> target).

3. **Cross-Query Aggregation**: For each distinct `Manufacturer` that is part of a valid supply chain, aggregate the data to find the single *cheapest* complete supply chain (Supplier -> Manufacturer -> Retailer) that passes through them. The cost of a supply chain is the sum of the `cost` of its two connecting edges.

4. **Query Result Export**: Your script must export these optimal supply chains to a JSON file at `/home/user/optimized_chains.json`. The JSON should be an array of objects, sorted by `total_cost` in strictly ascending order. Each object must exactly match this structure:
   ```json
   {
       "manufacturer": "<node_id>",
       "supplier": "<node_id>",
       "retailer": "<node_id>",
       "total_cost": <float>
   }
   ```

Constraints:
- Use only standard Python libraries (e.g., `sqlite3`, `json`). You do not need external dependencies like `pandas` or `networkx`.
- Ensure `/home/user/optimized_chains.json` is formatted as a valid JSON array.
- Run your script to generate the final JSON file.