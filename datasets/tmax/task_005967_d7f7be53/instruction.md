You are a data engineer building a graph-based ETL pipeline. You have been provided with a SQLite database at `/home/user/network.db` containing a social network graph. 

Your goal is to extract a specific subgraph, process it using a custom C program to find specific graph structures, and output a validated JSON report.

**Phase 1: Schema Analysis and Subgraph Extraction**
The database has two tables:
- `nodes` (`node_id` INTEGER PRIMARY KEY, `status` TEXT, `properties` TEXT)
- `edges` (`source` INTEGER, `target` INTEGER, `relation` TEXT)

Write a SQL query to extract all directed edges where:
1. Both the source and target nodes have a `status` of 'active'.
2. The `relation` is exactly 'follows'.

Export this subgraph as a comma-separated values (CSV) file at `/home/user/active_edges.csv` with no headers, formatted exactly as `source,target`.

**Phase 2: Graph Processing in C**
Write a C program at `/home/user/find_triangles.c` that reads `/home/user/active_edges.csv`.
The program must identify all directed triangles in the extracted graph. A directed triangle exists if there are edges A -> B, B -> C, and C -> A.
To avoid duplicates, for each triangle, normalize the representation by ordering the three nodes in ascending numerical order, but ONLY output the triangle if it forms a valid directed cycle.
Print each triangle to standard output as a JSON line:
`{"triangle": [min_id, mid_id, max_id]}`

Compile your program to `/home/user/find_triangles` and run it, saving its output to `/home/user/triangles.jsonl`.

**Phase 3: Aggregation and Schema Validation**
Using `jq` (a NoSQL-style JSON processor), aggregate the `triangles.jsonl` file into a single JSON report at `/home/user/final_report.json`.
The final JSON must perfectly match this schema:
```json
{
  "metadata": {
    "total_triangles": <integer_count_of_triangles>
  },
  "data": [
    [min_id, mid_id, max_id],
    ...
  ]
}
```
The arrays in the `data` list must be sorted lexicographically (first by min_id, then mid_id, then max_id).