You are a data analyst working with corporate ownership data extracted into CSV files. You need to perform graph analysis to determine supply chain dependencies and corporate structures. 

The data is located in `/home/user/data/` and consists of two files:
1. `entities.csv` - Contains the nodes of our knowledge graph.
   Columns: `id,name,industry`
2. `relationships.csv` - Contains the edges.
   Columns: `parent_id,child_id,relationship_type,ownership_percentage`

Your task is to write a Go program (e.g., `/home/user/analyze.go`) that performs the following pipeline:

**Step 1: Graph Construction & Filtering**
Parse the CSV files and build a directed knowledge graph. Filter the relationships to ONLY include edges where:
- `relationship_type` is exactly `"owns"`
- `ownership_percentage` is strictly greater than `50` (i.e., majority ownership).

**Step 2: Shortest Path Computation**
Find the shortest path (fewest number of hops/edges) from the entity named `"Apex_Holdings"` to the entity named `"Zeta_Retail"` using your filtered directed graph. 
Write the comma-separated names of the entities in this path (from start to finish) to `/home/user/shortest_path.txt`.
*(Note: If there are multiple shortest paths of the same length, your code should be deterministic, but for this specific dataset there is only one uniquely shortest path).*

**Step 3: Result Sorting, Filtering & Pagination**
Find all unique entities that are successfully reachable from `"Apex_Holdings"` in the filtered graph (excluding `"Apex_Holdings"` itself).
Sort these reachable entity names strictly alphabetically (A-Z).
Implement pagination with a page size of exactly `2` records per page.
Extract Page 2 (which should contain the 3rd and 4th alphabetically sorted entities).
Write these two entity names to `/home/user/page2.txt`, with one name per line.

Ensure your Go program operates natively using the standard library (or popular external modules if you fetch them via `go mod init` and `go get`). You must run your Go program so that the final output files are created in the correct location.