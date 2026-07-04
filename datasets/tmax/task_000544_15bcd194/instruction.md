You are a database administrator tasked with optimizing and integrating queries across a hybrid data architecture. We have a relational SQLite database (`/home/user/ecommerce.db`) and a file containing NoSQL-style event logs in JSON Lines format (`/home/user/activity.jsonl`). 

Your objective is to write a Python script `/home/user/analyze_path.py` that connects these disparate data sources to perform a unified analysis. The script must be run to generate a final report.

Here is the schema for `/home/user/ecommerce.db`:
- Table `users`: `id` (INTEGER PRIMARY KEY), `name` (TEXT)
- Table `friendships`: `user_id1` (INTEGER), `user_id2` (INTEGER)  -- represents an undirected graph of user connections. If (A, B) exists, A and B are friends.
- Table `purchases`: `id` (INTEGER PRIMARY KEY), `user_id` (INTEGER), `amount` (REAL)

The NoSQL logs in `/home/user/activity.jsonl` have the following structure:
`{"user_id": INT, "event": STR, "duration_ms": INT, "metadata": {...}}`

Your script `/home/user/analyze_path.py` must perform the following operations:
1. **Graph Traversal:** Compute the shortest path (in terms of number of edges) between user ID `1` and user ID `20` using the `friendships` table. (Assume a path exists and there is only one uniquely shortest path).
2. **Complex SQL Query:** For *only* the users present in that shortest path, execute a query against the SQLite database to retrieve their `name` and their total combined `amount` of purchases. You must use a single query with JOINs and aggregation.
3. **NoSQL Aggregation Pipeline:** Parse the `activity.jsonl` file. Implement an aggregation (using Python dictionaries, `pandas`, or `duckdb`) that processes only the logs belonging to the users in the shortest path. You need to group the records by `user_id` and then by `event`, calculating the average (mean) `duration_ms` for each event type per user.
4. **Output Generation:** Combine all this information into a single JSON file located at `/home/user/report.json`.

The format of `/home/user/report.json` must exactly match this structure:
```json
{
  "path": [1, 5, 8, 20],
  "purchases": {
    "1": {
      "name": "Alice",
      "total_spent": 250.5
    },
    ...
  },
  "activity_aggregation": {
    "1": {
      "click": 105.0,
      "scroll": 500.2
    },
    ...
  }
}
```
*Note: The keys in "purchases" and "activity_aggregation" must be string representations of the user IDs. The average durations should be floats.*

Run your script to generate the `/home/user/report.json` file. Ensure the script handles potential missing events gracefully (e.g., if a user has no purchases, `total_spent` should be `0.0` or missing entirely depending on the JOIN, but for this task, assume all path users have at least one purchase and activity).