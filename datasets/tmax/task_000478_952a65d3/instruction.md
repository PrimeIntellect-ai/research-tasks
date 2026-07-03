You are an AI assistant helping a researcher analyze a biological network dataset. 

The researcher has an SQLite database at `/home/user/network.db` containing an un-documented graph. By examining the database, you need to reverse engineer its schema (there are tables for vertices and directed edges).

Your task is to write a Python script `/home/user/analyze_network.py` that performs complex graph queries on this database.

The script must accept the following command-line arguments:
`--start`: The name of the starting node.
`--end`: The name of the target node.
`--max-hops`: The maximum number of edges allowed in a path.

The script should perform the following operations using SQLite queries (leveraging recursive CTEs where appropriate):
1. Find all valid directed paths from the `--start` node to the `--end` node that contain at most `--max-hops` edges.
2. Calculate the total weight/cost of each path.
3. Determine the shortest path (the one with the minimum total weight) among the valid paths.
4. Output the result to `/home/user/shortest_path.json` in the exact following format:
```json
{
  "path": ["StartNodeName", "IntermediateNode1", "IntermediateNode2", "EndNodeName"],
  "total_weight": 15.5
}
```
If there are multiple paths with the exact same minimum weight, output any one of them. If no path exists within the hop limit, output `{"path": [], "total_weight": null}`.

To test your script, run it with:
`python3 /home/user/analyze_network.py --start "Protein_A" --end "Disease_Z" --max-hops 3`

Ensure your script handles parameterized queries safely to prevent SQL injection, and properly closes database connections. Leave the final output file `/home/user/shortest_path.json` generated for this test case on disk for verification.