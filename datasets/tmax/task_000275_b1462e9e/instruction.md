You are a data analyst tasked with processing a temporal graph dataset. 

Our legacy system used an SQLite database to store network transactions. However, a corrupted B-tree index in the system caused it to return stale and incorrect rows, so we have dumped the raw data to a CSV file at `/app/data/network.csv`.

We have a proprietary compiled tool, located at `/app/graph_oracle`, which computes a "Temporal Impact Score" for any given node ID. Unfortunately, the source code was lost, the binary is stripped, and it is far too slow to run iteratively for the entire dataset (it takes seconds per node). 

Your task is to:
1. Reverse-engineer or deduce the logic of the Temporal Impact Score by testing `/app/graph_oracle` with different node IDs (it accepts a single node ID as a command-line argument and prints the score).
2. Write a highly optimized Python script at `/home/user/calculate_scores.py` that reads `/app/data/network.csv`.
3. Your script must use SQL window functions and analytical aggregations (you may use `duckdb` or `sqlite3` in Python) to calculate the Temporal Impact Score for **every** unique target node in the dataset.
4. Export the final query results to a CSV file at `/home/user/results.csv`. The output CSV must have exactly two columns: `node_id` (integer) and `impact_score` (float).

The `/app/data/network.csv` file has the following columns:
- `source_id` (int)
- `target_id` (int)
- `timestamp` (int, UNIX epoch)
- `weight` (float)

Your solution must be computationally efficient. An automated verifier will calculate the Mean Squared Error (MSE) between your `results.csv` and the true values. Your script should execute and generate the file cleanly.