You are assisting a researcher who is organizing a massive collection of dataset citation networks and knowledge graphs. Several months ago, they compiled a highly optimized C++ tool to compute custom graph analytics (dataset centrality, co-citation clustering, and knowledge graph pattern matching). 

Unfortunately, they lost the source code and are left only with a stripped binary located at `/app/dataset_analyzer`. 

Your task is to reverse-engineer the behavior of this binary and write a functionally identical C++ program.

The binary reads a directed graph and a list of queries from standard input (`stdin`) and writes the results to standard output (`stdout`). 

**Input Format:**
1. The first line contains two integers: `V` (number of vertices/datasets, 0-indexed) and `E` (number of directed edges).
2. The next `E` lines each contain two integers `u` and `v`, representing a directed edge from `u` to `v`.
3. The next line contains an integer `Q`, the number of queries.
4. The next `Q` lines contain queries in one of the following formats:
   - `CENTRALITY u`
   - `CO_CITE u v`
   - `PATTERN u`

**Output Format:**
For each query, the binary outputs a single integer on a new line.

**Requirements:**
1. Interact with the binary using small, custom inputs to deduce exactly what mathematical graph metric each query calculates.
2. Write a C++ source file at `/home/user/solution.cpp` that implements these exact metrics. Note that the real networks are large, so you must implement an efficient indexing strategy (e.g., adjacency lists) rather than brute-forcing `O(V^3)` operations.
3. Compile your code to `/home/user/solution` using `g++ -O3 -std=c++17 /home/user/solution.cpp -o /home/user/solution`.

Your solution will be tested against the original binary using a rigorous fuzzing suite with thousands of random graphs and edge cases. Its standard output must perfectly match the oracle binary byte-for-byte.