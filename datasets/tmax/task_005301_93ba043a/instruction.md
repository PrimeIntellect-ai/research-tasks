You are a data analyst working for a logistics company. You have been provided with a CSV file at `/home/user/network.csv` that contains routing data for the company's delivery network.

The CSV has the following columns: `source`, `target`, `time`, `cost`. 

Your task is to write a Python script at `/home/user/route_optimizer.py` that processes this data to find the optimal delivery route. 

The script must meet the following requirements:
1. It must accept exactly three command-line arguments in this order: `start_node`, `end_node`, `max_edge_cost`. (e.g., `python3 /home/user/route_optimizer.py A D 15`)
2. It must load the data from `/home/user/network.csv` into a local SQLite database (in-memory or file-backed).
3. It must use a **parameterized SQL query** to retrieve only the edges where the `cost` is less than or equal to `max_edge_cost`.
4. Using the retrieved edges, it must compute the shortest path from `start_node` to `end_node` that minimizes the total `time`. You may use Python's built-in libraries or standard graph traversal algorithms (like Dijkstra's).
5. It must export the resulting path and its total time to a JSON file at `/home/user/optimal_route.json`.

The exported JSON file must have exactly this structure:
```json
{
  "path": ["node1", "node2", "node3"],
  "total_time": 42
}
```
If no valid path exists under the cost constraint, `path` should be an empty list `[]` and `total_time` should be `null`.

Please write and execute your script to verify it works, but do not leave it running interactively. You do not need to submit the final output file manually; simply leave the correct `/home/user/route_optimizer.py` script on the system so we can test it against our own parameters.