I am a data analyst studying financial exposure networks using large CSV exports of our knowledge graph. I need a high-performance C utility to calculate the "Recursive Pattern Exposure" starting from any given node.

I downloaded a lightweight C library for parsing and traversing CSV-based graphs called `libgraphcsv` v1.2.0, and its source is located at `/app/libgraphcsv-1.2.0`. However, I'm having two problems:
1. When I build and test it, recursive hierarchical queries silently stop after exactly 3 hops, even though the graph is much deeper. I suspect there is a hardcoded limit or a misconfiguration in the library's build system or source code that needs to be fixed so it can support at least 100 hops. You need to fix this library and install it system-wide (or locally so my program can link against it).
2. I need you to write the main application at `/home/user/exposure_calculator.c` and compile it to `/home/user/exposure_calculator`.

The utility `/home/user/exposure_calculator` must take exactly two command-line arguments:
1. `csv_path`: The path to a CSV file representing the graph edges.
2. `start_node`: A string representing the starting Node ID.

**Data Format:**
The CSV file (e.g., `transactions.csv`) has no header and contains edges in the format:
`SourceNodeID,TargetNodeID,TargetNodeType,Weight`
Example:
`ENT_001,ACC_104,ACCOUNT,500`

**Logic / Calculation:**
You must implement a cross-query aggregation using recursive knowledge graph pattern matching. Starting from `start_node`, traverse the directed graph recursively. You must aggregate (sum) the `Weight` of all valid paths.
A path is only valid (and its final edge's weight added to the total) if it strictly alternates node types in the sequence: `ACCOUNT` -> `COMPANY` -> `ACCOUNT` -> `COMPANY`... and so on.
- The first edge traversed from `start_node` must point to a node of type `ACCOUNT`.
- The next edge from that node must point to a node of type `COMPANY`.
- The next must be `ACCOUNT`, and so on.
- If an edge violates this pattern, do not traverse it.
- Cycles should be avoided (do not visit the same Node ID twice in a single path).
- Sum the `Weight` of every valid edge traversed during this pattern matching.

Print *only* the final total integer weight to standard output. 

Please fix the library, compile your program linking to the fixed library, and ensure it prints the exact correct aggregated integer.