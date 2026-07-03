You are an analyst tasked with processing a network dataset provided as CSV files, but the dataset contains stale rows that need to be filtered out before graph materialization.

You have three CSV files in `/home/user/`:
1. `nodes.csv` (columns: `node_id`, `name`)
2. `edges.csv` (columns: `src`, `dst`, `cost`, `version`)
3. `tombstones.csv` (columns: `src`, `dst`, `version`)

Your task is to write a C program that:
1. Reads these files and filters out stale edges. An edge is considered "deleted" (stale) if there is an entry in `tombstones.csv` with the exact same `src` and `dst` and a `version` strictly greater than or equal to the edge's `version`.
2. If there are multiple undeleted edge records for the same `src` and `dst`, keep only the one with the highest `version`.
3. Projects this filtered relational data into an in-memory directed graph (edges are directed from `src` to `dst`).
4. Computes the shortest path from node `10` to node `42` based on the `cost` field.
5. Outputs the resulting path and total cost as a JSON document to `/home/user/path.json`.

The expected format of `/home/user/path.json` is:
```json
{
  "path": [10, ...other_nodes..., 42],
  "cost": 123
}
```

Constraints:
- Do not use any external C libraries other than the standard library (e.g., `<stdio.h>`, `<stdlib.h>`, `<string.h>`, etc.).
- The output JSON file must be strictly formatted with double quotes for keys and no trailing commas.
- Assume all costs are non-negative integers.

Write, compile, and execute your C program to generate the required JSON file.