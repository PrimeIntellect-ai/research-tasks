You are a Database Administrator and Data Engineer optimizing a new graph-based analytics pipeline. We are migrating away from a heavy NoSQL aggregation pipeline into an in-memory graph processing model, and we need a prototype script to prove the logic.

Your task is to write and execute a Python script (`/home/user/process_graph.py`) that performs the following steps:

1. **Simulate a NoSQL Aggregation Pipeline:**
   Read a JSONL file located at `/home/user/data/events.jsonl`. Each line is a JSON object representing a user interaction (keys: `user_id`, `item_id`, `event_type`, `timestamp`).
   Filter the records to keep only those where `event_type` is exactly `"purchase"`. 

2. **Knowledge Graph Pattern Extraction:**
   From the filtered purchase events, extract a co-purchase item graph. 
   Create an undirected graph where nodes are `item_id`s. Add an edge between two items if there is at least one `user_id` who has purchased both items. (Ignore self-loops).

3. **Graph Analytics:**
   Use the `networkx` library to compute the unweighted Degree Centrality for every node (item) in the resulting graph. 

4. **Parameterized Query Construction:**
   Create a SQLite database at `/home/user/output/analytics.db`.
   Create a table named `item_centrality` with two columns: `item_id` (TEXT) and `centrality` (REAL).
   Find the top 3 items with the highest degree centrality. If there are ties, sort them alphabetically by `item_id` ascending.
   Using the `sqlite3` module in Python, insert these top 3 items and their centrality scores into the `item_centrality` table using **parameterized queries** (e.g., `INSERT INTO ... VALUES (?, ?)`).

**Setup:**
* The input data `/home/user/data/events.jsonl` will be present on the system.
* You may need to install `networkx` using pip if it is not already installed.
* Ensure all outputs are written exactly to `/home/user/output/analytics.db`. 

Execute your script to produce the final SQLite database before concluding the task.