You are assisting a researcher who is organizing a dataset of academic citations. The data is stored in an SQLite database located at `/home/user/citation_graph.db`. 

However, the researcher has encountered a few problems:
1. They lost the schema documentation, so you must reverse engineer the data model by inspecting the database. The database contains a table for papers (nodes) and a table for citations (edges), but their exact names and column definitions are unknown.
2. Due to a botched migration in the past, the database has a "corrupted" state: the table representing citations contains duplicate rows that should not exist. The original unique index was accidentally dropped, causing queries to return stale/duplicate relationships. 

Your objectives are:
1. **Database Repair**: Inspect the database to find the node and edge tables. Remove all exact duplicate rows from the edge table (keeping only one instance of each source-target pair). Then, create a `UNIQUE` index on the source and target columns to prevent future duplicates.
2. **Graph Analytics in C**: Write a C program named `/home/user/graph_analyzer.c` that connects to this SQLite database using the SQLite3 C API.
3. **Centrality Calculation**: In your C program, calculate the total degree centrality (in-degree + out-degree) for every node in the repaired graph. (Note: an edge from A to B counts as +1 out-degree for A and +1 in-degree for B. Total degree is the sum of both).
4. **Schema Validated Output**: Your C program must find the top 3 nodes with the highest total degree centrality and output the results strictly as a JSON file to `/home/user/top_nodes.json`. 

The output JSON must exactly match this schema:
```json
{
  "top_nodes": [
    {
      "node_id": 123,
      "degree": 10
    },
    {
      "node_id": 456,
      "degree": 8
    },
    {
      "node_id": 789,
      "degree": 7
    }
  ]
}
```
(Ensure the nodes are ordered from highest degree to lowest. If there is a tie, order by `node_id` ascending).

**Constraints & Notes:**
* You have full permissions in `/home/user/`.
* You may install any necessary dependencies (e.g., `gcc`, `libsqlite3-dev`) using the standard package manager.
* Compile your program to `/home/user/graph_analyzer` and execute it to generate the JSON file.