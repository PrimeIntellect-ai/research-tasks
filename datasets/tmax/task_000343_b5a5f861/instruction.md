You are a data analyst tasked with generating a reporting structure report for the HR department. You have been provided with two CSV files: `/home/user/nodes.csv` and `/home/user/edges.csv`.

An intern previously attempted to write a script to find the management chain from every employee up to the CEO (Node ID: `E001`). However, their script had a logic flaw: it ignored the relationship types. Because employees have multiple types of relationships (e.g., 'colleague', 'friend', 'reports_to'), the intern's script acted like an implicit cross join, resulting in a combinatorial explosion of invalid paths and cyclic loops.

Your task is to write a Python script (e.g., `/home/user/solve.py`) that correctly computes the hierarchical paths and exports the results.

Requirements:
1. Parse the CSV files. The graph is directed.
2. Calculate the shortest path from every employee to the CEO (`E001`).
3. **Crucial:** You must ONLY traverse edges where the `relation_type` is exactly `reports_to`. Ignore all other relationship types.
4. Filter the results to ONLY include employees whose shortest path to the CEO requires 2 or more hops (where hops = number of edges traversed, meaning the path contains 3 or more nodes).
5. Sort the final filtered results by the starting `employee_id` in ascending alphabetical order.
6. Export the output to `/home/user/verified_paths.json`.

The final JSON file must strictly adhere to the following format (a JSON array of objects):
```json
[
  {
    "employee_id": "E00X",
    "hops": 2,
    "path": ["E00X", "E00Y", "E001"]
  }
]
```

Write your code, execute it, and ensure the resulting `/home/user/verified_paths.json` exists and is correctly formatted.