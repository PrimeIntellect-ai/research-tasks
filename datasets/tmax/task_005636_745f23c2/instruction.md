You are a database administrator working on optimizing queries. You have exported your database's execution plan dependencies into a simple text-based Knowledge Graph format, but your usual query tools are unavailable on this locked-down server.

You have a file at `/home/user/dependencies.tsv`. This file represents a directed graph using tab-separated Triples (`Subject \t Predicate \t Object`).

Your task is to write a C program at `/home/user/graph_query.c` that parses this file and finds the names of all database tables that are being accessed via a "sequential_scan".

Specifically, you need to find all subjects `X` that satisfy the following graph pattern:
1. `X` has the relation `type` -> `table`
2. `X` has the relation `scanned_by` -> `Y`
3. `Y` has the relation `type` -> `sequential_scan`

Once you have identified all such tables (`X`), your C program must:
1. Sort the names of these tables alphabetically (ascending).
2. Paginate the results by applying an OFFSET of 2 and a LIMIT of 3. (i.e., skip the first 2 sorted results, and take up to the next 3).
3. Export the resulting paginated list as a strictly formatted JSON array of strings to a file named `/home/user/results.json`.

Example of the expected output format for `/home/user/results.json`:
```json
[
  "table_c",
  "table_d",
  "table_e"
]
```

Requirements:
- Your solution must be written in standard C (`/home/user/graph_query.c`).
- You can compile it using `gcc`.
- It must read from `/home/user/dependencies.tsv` and write to `/home/user/results.json`.
- Do not use any external dependencies outside of the C standard library.