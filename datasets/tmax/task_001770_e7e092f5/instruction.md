As a compliance officer auditing our internal systems, I need to investigate a potential violation of separation of duties. We have a flat log file of access delegations, but no clear map of the overall access network. 

I need you to reverse-engineer the access graph from our delegation logs, aggregate some overall network metrics, and find the shortest path of delegations between two specific users.

You have access to a CSV file located at `/home/user/delegations.csv`. 
The CSV has the following headers: `delegator,delegatee,timestamp`

Please write a Python script at `/home/user/audit.py` that does the following:
1. Reads the `delegations.csv` file.
2. Reconstructs a directed graph of delegations (where an edge goes from `delegator` to `delegatee`).
3. Computes the total number of unique users (both delegators and delegatees) present in the entire log.
4. Computes the shortest path (fewest number of edges) from the user `User_Charlie` to the user `User_Zulu`. If there are multiple paths of the same shortest length, any of them is acceptable.

The script must execute and output the results to a JSON file at `/home/user/audit_report.json` with the exact following schema:

```json
{
  "total_unique_users": <integer>,
  "shortest_path": ["User_Charlie", "...", "User_Zulu"]
}
```

Write the script, run it, and ensure the `audit_report.json` file is successfully generated. Standard library modules are preferred, but if you need an external library like `networkx`, you may install it.