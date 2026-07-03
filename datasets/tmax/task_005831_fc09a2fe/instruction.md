You are assisting a researcher who is organizing a large scientific dataset representing a citation network. The data was previously housed in an SQLite database, but a corrupted index caused it to return stale and duplicated rows. The researcher exported the raw table to a CSV file to process manually.

The exported data is located at `/home/user/citation_graph.csv`. 

Your task is to write a C program that processes this graph, filters out the stale data, computes the hierarchical dependencies, and outputs a specific paginated result.

Here are the requirements for your C program (`/home/user/graph_tool.c`):

1. **Schema Validation**: 
   The program must first read the header of the CSV file. If the header is not exactly `edge_id,child,parent,timestamp,is_active`, the program must print an error and exit with code `2`.

2. **Data Filtering (Stale Rows)**:
   - Ignore any row where `is_active` is `0`.
   - The corrupted index caused duplicate `(child, parent)` edges to be exported. If there are multiple active rows for the same `(child, parent)` pair, you must strictly use the one with the highest `timestamp`. (Note: in this dataset, a higher timestamp means the edge was verified more recently; you only include a parent-child relationship if the most recent active record confirms it. Wait, actually, just deduplicate and consider the edge exists). 

3. **Recursive/Hierarchical Query**:
   Build the directed graph (from `parent` to `child`). 
   Find all unique descendants of the root node `"ROOT"`.
   Calculate the shortest path depth for each descendant relative to `"ROOT"` (where `"ROOT"` is depth 0, its immediate children are depth 1, etc.).

4. **Result Sorting and Pagination**:
   Sort the resulting descendants primarily by `depth` in ascending order, and secondarily by the `child` node's string name in ascending lexicographical order.
   The researcher only wants to see a specific "page" of results. Implement pagination with a page size of `10`.
   Output **only Page 2** (which means skipping the first 10 results and outputting results 11 through 20). If there are fewer than 11 results, output nothing. If there are between 11 and 20 results, output whatever is available on that page.

5. **Output Schema Validation**:
   The output must be written to `/home/user/page2.csv`.
   It must include a header: `node,depth`
   Followed by the comma-separated values for the 10 nodes on page 2.

Compile your program to `/home/user/graph_tool` and run it to generate the output file.