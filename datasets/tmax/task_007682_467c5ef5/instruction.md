You are acting as a data analyst working on logistics optimization. You have been provided with a dataset of transit times between various distribution hubs in a CSV format. 

Your task is to build a high-performance graph processing tool in C to analyze this logistics network and compute the optimal (shortest) transit route between two specific hubs.

Here are your instructions:

1. **Input Data**: The input data is located at `/home/user/hub_transit_data.csv`. It has the following structure (with a header row):
   `source_hub,destination_hub,transit_time`
   (e.g., `Seattle,Denver,10`)
   Note that the connections are directed (a route from A to B does not imply a route from B to A with the same time, though they may exist).

2. **C Program Requirements**: 
   Write a C program at `/home/user/route_solver.c` that does the following:
   - Implements a string-to-integer indexing strategy (e.g., a hash map or sorted array) to dynamically map hub names from the CSV to integer node IDs.
   - Parses the CSV and projects the data into an in-memory graph representation (e.g., an adjacency list) suitable for fast traversal.
   - Implements Dijkstra's algorithm to compute the shortest path (minimum total transit time) from **"Seattle"** to **"Miami"**.
   - Your program must handle up to 100 unique hubs and 1000 edges.

3. **Execution & Output**:
   Compile your C program into an executable named `/home/user/route_solver` using `gcc`. Run the executable. 
   The program must write its final output to a log file located at `/home/user/shortest_path.log`. 
   
   The log file must exactly follow this format:
   ```
   Shortest Transit Time: [TOTAL_TIME]
   Route: [Hub1] -> [Hub2] -> ... -> [HubN]
   ```
   For example:
   ```
   Shortest Transit Time: 45
   Route: Seattle -> Dallas -> Atlanta -> Miami
   ```

Do not use any external graph processing libraries (like igraph). You must implement the data structures, index strategy, and shortest-path logic yourself using standard C libraries (`stdio.h`, `stdlib.h`, `string.h`, etc.).