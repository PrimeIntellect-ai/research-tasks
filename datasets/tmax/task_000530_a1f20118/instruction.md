You are a data engineer building a high-performance ETL pipeline and query engine for a dynamic logistics network.

We have received the initial network topology as an image of a data table, located at `/app/init_topology.png`. 

Your task involves several steps:
1. **Extract Initial Data**: Extract the edge data from `/app/init_topology.png`. The image contains a table with columns `Source`, `Target`, and `Cost` (in that order). Save this data as a CSV file named `/home/user/init_graph.csv` (comma-separated, no headers).
2. **Process Updates**: There is a file `/app/updates.csv` containing network changes in the format `Action,Source,Target,Cost`. Actions can be `ADD`, `DEL`, or `UPD`.
3. **Execute Queries**: There is a file `/app/queries.csv` containing routing queries in the format `Source,Target`.
4. **Implement Query Engine in C**: Write a C program at `/home/user/query_engine.c` that:
   - Reads the initial graph from the CSV file you created.
   - Applies the updates from `/app/updates.csv` sequentially.
   - Computes the shortest path cost for each query in `/app/queries.csv`.
   - Exports the results to `/home/user/results.json` as a JSON array of objects, e.g., `[{"src": 1, "dst": 2, "cost": 15.5}, ...]`. If no path exists, output `-1.0` for the cost.
5. **Compile**: Compile your program to an executable named `/home/user/query_engine`. It must accept arguments exactly as follows:
   `./query_engine <init_graph.csv> <updates.csv> <queries.csv> <output.json>`

Your C implementation must be highly optimized. The automated verifier will replace `/app/updates.csv` and `/app/queries.csv` with massive, hidden datasets (tens of thousands of nodes and hundreds of thousands of queries) and measure your program's execution time. Your program must finish execution under the required threshold (0.5 seconds for the hidden dataset).

**Constraints & Details**:
- Nodes are non-negative integers up to 100,000.
- Costs are floating-point numbers.
- The graph is directed.
- You may use any standard Linux tools (like `tesseract`) to help with the image extraction.
- Do not use external C libraries for the graph processing (standard C library only).