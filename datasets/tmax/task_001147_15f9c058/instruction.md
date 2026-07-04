You are acting as a data analyst and C++ developer. We have a logistics network represented by a set of CSV files. You need to write a high-performance C++ program that ingests this graph data, processes a batch of routing queries, and computes cross-query aggregations. 

Please perform the following steps:

1. **Workspace Setup:**
   Create a directory at `/home/user/logistics_graph` and do all your work inside it.

2. **Input Data Understanding:**
   You will find three input files already present in `/home/user/logistics_graph/data/` (you should assume these exist during compilation, though you may create dummy ones to test your code):
   - `nodes.csv`: Contains two columns `node_id,node_name`. (e.g., `N1,Warehouse_A`)
   - `edges.csv`: Contains four columns `source_id,target_id,distance,cost`. The graph is **directed**. (e.g., `N1,N2,15.5,100.0`)
   - `queries.csv`: Contains two columns `source_id,target_id` representing the shortest path queries we want to run.

3. **C++ Application Requirements:**
   Write a C++17 program (e.g., `main.cpp`) that:
   - Reads the CSV files.
   - Implements an efficient in-memory index strategy (e.g., using hash maps) to map the string-based `node_id`s to internal memory-contiguous integer representations for fast traversal.
   - Uses Dijkstra's algorithm to compute the shortest path based strictly on **distance** (ignore cost for the routing metric, but accumulate the cost along the chosen path).
   - If multiple paths have the exact same shortest distance, pick any valid one (our test data has unique shortest paths).
   - Processes all queries defined in `queries.csv`.

4. **Output Generation:**
   Your program must produce two exact output files in `/home/user/logistics_graph/output/` (create this directory if it doesn't exist):
   
   **A. `results.csv`**:
   Format: `source_id,target_id,total_distance,total_cost,path`
   Where `path` is the sequence of `node_id`s separated by hyphens (e.g., `N1-N3-N2`). If no path exists, write `source_id,target_id,-1,-1,NONE`.
   
   **B. `summary.txt`**:
   Compute cross-query aggregations for all **successfully routed** queries.
   Format exactly as follows:
   ```
   Successful Queries: [count]
   Failed Queries: [count]
   Total Accumulated Distance: [sum_of_distances]
   Total Accumulated Cost: [sum_of_costs]
   ```
   (Format floats to 1 decimal place).

5. **Build & Execute:**
   Provide a bash script `/home/user/logistics_graph/run.sh` that compiles your C++ code with `-O3 -std=c++17` using `g++` and runs the executable.

You do not need to use external libraries (like Boost) for this; standard C++17 is sufficient.