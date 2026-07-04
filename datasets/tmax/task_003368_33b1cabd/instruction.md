You are acting as a data engineer for a knowledge graph platform. We export graph data into massive CSV files and allow analysts to query them by defining graph pattern matching workflows. 

However, we are experiencing severe performance issues. Analysts are submitting query batches that contain "implicit cross-joins" (disconnected graph patterns). When translated into our pipeline, these patterns cause catastrophic Cartesian products.

Your task is to build a C-based Query Batch Sanitizer that parses batch query CSV files and rejects batches containing any disconnected query patterns.

**Part 1: Fix the Vendored CSV Library**
We use `libcsv` to parse the batch files. The source code is vendored at `/app/libcsv-3.0.3`. 
1. The previous developer left it in a broken state (it fails to compile via `make`).
2. Identify and fix the perturbation in the source code.
3. Build and install the library so it can be linked by your C program.

**Part 2: Implement the Query Sanitizer in C**
Write a C program at `/home/user/detector.c` and compile it to `/home/user/detector`. 
It must dynamically link against the fixed `libcsv`.

The tool must accept exactly one argument: the path to a batch CSV file.
Execution format: `/home/user/detector <path_to_csv>`

**Batch CSV Format:**
The CSV files have two columns and a header: `query_id,edge_pattern`
Example:
```csv
query_id,edge_pattern
q1,A:B;B:C;C:A
q2,X:Y;Z:W
```
* `edge_pattern` represents undirected edges in a knowledge graph query. Nodes are uppercase alphanumeric strings (up to 4 chars). Edges are separated by semicolons (`;`), and nodes in an edge are separated by colons (`:`).
* If a query defines a graph with more than one connected component (like `q2` above, where `X:Y` is disconnected from `Z:W`), it implies a cross-join.

**Sanitizer Logic:**
Your C program must use `libcsv` to parse the CSV file.
For each row (skipping the header):
1. Parse the `edge_pattern`.
2. Determine if the graph represented by the edges forms a **single connected component**.
3. If **any** query in the CSV file is disconnected (meaning it has 2 or more separate components), the tool must immediately exit with status code **1** (Rejected).
4. If **all** queries in the CSV file represent single connected components, the tool must exit with status code **0** (Accepted).
5. Single-edge queries (e.g., `A:B`) are always connected. 

**Verification:**
Your compiled `/home/user/detector` will be tested against two sets of CSV files:
- A "clean" corpus of valid batches.
- An "evil" corpus of batches containing hidden cross-joins.
You must ensure it perfectly accepts the clean corpus and rejects the evil corpus.