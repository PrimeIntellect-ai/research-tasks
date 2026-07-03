You are a data analyst tasked with processing an employee reporting hierarchy from a CSV file. 

You have been provided with a file at `/home/user/employee_edges.csv`. This file acts as an event log of management changes. Because it's an append-only log, it contains "stale" rows. 

The CSV has the following columns:
`manager,employee,timestamp`

An employee can only have **one** direct manager at any given time. The true, current manager for any `employee` is the one specified in the row with the **highest `timestamp`** for that employee.

Your task is to:
1. Parse the CSV file using Python and filter out the stale rows to reconstruct the current, valid management graph.
2. Perform a recursive/hierarchical query on this graph to find "Alice" and all of her direct and indirect reports (her entire downstream organization).
3. Export this specific subgraph (Alice and all her descendants) to a JSON file at `/home/user/alice_team.json`.

To ensure your output passes our schema validation, the JSON file must strictly match this format:
```json
{
  "nodes": ["A", "B", ...],
  "edges": [
    {"manager": "A", "employee": "B"},
    ...
  ]
}
```

Constraints for the output JSON:
- `nodes` must be a flat list of employee names in the subgraph (including Alice), sorted alphabetically.
- `edges` must be a list of objects representing the management links in the subgraph. This list must be sorted alphabetically by `manager`, and then by `employee`.
- Only include edges where both the manager and the employee are part of Alice's organization (i.e., Alice or her descendants).

Write and execute a Python script to perform this data processing and produce the final `/home/user/alice_team.json` file.