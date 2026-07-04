You are acting as a data analyst and backend engineer. We have a system that processes a high volume of financial transactions represented as a graph, where accounts are nodes and transactions are edges. Recently, concurrent transactions have been creating cyclical deadlocks in our processing pipeline. To resolve this, we need to analyze the most liquid paths between accounts.

You have been given a dataset `/home/user/transactions.csv` with the following columns: `tx_id,src_account,dst_account,amount,status,timestamp`.
You also have a list of queries in `/home/user/queries.json`, which is an array of objects: `[{"src": "A", "dst": "B"}, ...]`.

There is an existing, highly unoptimized reference binary located at `/app/path_oracle`. This binary is stripped, but it processes the CSV and queries to find the "shortest" (most liquid) paths. It is far too slow for production.

Your objective is to write a highly optimized Go program (`/home/user/processor.go`) that does the following:
1. Start a local MongoDB instance (using Docker: `docker run -d -p 27017:27017 mongo`).
2. Load the data from `transactions.csv` into a MongoDB database named `financial`, collection `transactions`.
3. Use a MongoDB NoSQL aggregation pipeline to fetch only valid edges: keep transactions where `status == 'completed'` and `amount >= 100`. If there are multiple completed transactions between the exact same `src` and `dst`, group them and sum their `amount` to create a single aggregated edge.
4. Build an in-memory directed graph using these aggregated edges. The "weight" (distance) of an edge from `src` to `dst` should be calculated as `1.0 / aggregated_amount` (so higher volume implies a "shorter" or more liquid path).
5. For every pair in `queries.json`, compute the shortest path using an optimized graph traversal algorithm (e.g., Dijkstra's).
6. Filter out any paths that require more than 6 hops (edges).
7. Sort the successfully found paths by their total weight in ascending order. If weights are equal, sort alphabetically by `src` then `dst`.
8. Paginate the result: extract only the top 50 paths (index 0 to 49).
9. Output the results to `/home/user/output.json` conforming strictly to this schema:
   ```json
   [
     {
       "src": "string",
       "dst": "string",
       "path": ["node1", "node2", "node3"],
       "total_weight": 0.00125
     }
   ]
   ```

Your Go program must compile to an executable and execute significantly faster than the reference binary while producing the exact same JSON output. Our automated verifier will measure your program's execution time against `/app/path_oracle`. You must achieve a minimum speedup of 4.0x.

Requirements:
- Your final code must be at `/home/user/processor.go`.
- You can install any standard Go packages you need (e.g., MongoDB driver).
- Do not run your script as root.