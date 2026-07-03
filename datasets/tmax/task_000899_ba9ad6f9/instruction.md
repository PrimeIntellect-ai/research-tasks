I am a researcher organizing a departmental collaboration graph dataset. I have two relational CSV files representing a co-authorship network, and I need to map this relational data into an analytical document format using Bash.

The files are located at:
1. `/home/user/nodes.csv` - Contains `node_id,author_name,department`
2. `/home/user/edges.csv` - Contains `source_id,target_id,weight` (representing directed collaboration edges and their strength)

I need you to write a Bash script at `/home/user/analyze.sh` that performs the following data querying and aggregation tasks using standard CLI tools (like `awk`, `join`, `sort`, `jq`, etc.):
1. Join the edges with the nodes to determine the department of both the source and target nodes.
2. Filter out internal collaborations (where the source and target departments are the same).
3. Aggregate the data to calculate the total outgoing external collaboration weight for each department.
4. Determine the "top partner" department for each department (the external department receiving the highest total weight from the source department). If there's a tie, you can pick any of the tied departments.
5. Export this aggregated view into a JSON array of objects, saved to `/home/user/output.json`.

The resulting `/home/user/output.json` must be a valid JSON array of objects, sorted alphabetically by the source `department` name. Each object should have the exact following schema:
```json
[
  {
    "department": "DepartmentName",
    "total_external_weight": 10,
    "top_partner": "OtherDepartmentName"
  }
]
```

Ensure your script is executable and can be run without any arguments. It should silently process the files and generate `/home/user/output.json`.