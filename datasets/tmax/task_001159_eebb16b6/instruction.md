You are a data analyst investigating a series of transaction records to identify potential collusion rings. You have a dataset of transactions, and you need to perform analytical aggregations and graph analysis using C++.

The input file is located at `/home/user/network.csv`. It has a header and the following columns:
`tx_id,source,target,amount,time_seq`

Your task is to write a C++ program that processes this data and identifies the largest network of suspicious actors. You must implement the following logic:

1. **Analytical Aggregation (Window Function Equivalent)**: 
   Read the CSV and calculate a running cumulative sum of `amount` for each `source` node, ordered by `time_seq` ascending. (Assume `time_seq` is unique per `source`). 
   *Conceptually, this is equivalent to the SQL: `SUM(amount) OVER (PARTITION BY source ORDER BY time_seq)`*.

2. **Graph Materialization & Filtering**:
   Project a graph by materializing undirected edges between `source` and `target` for **only** the transactions where the calculated running cumulative sum for the `source` (at the time of that transaction) is strictly greater than `150.0`. 

3. **Graph Component Analysis**:
   Using the materialized undirected edges, compute the connected components of the graph. Find the largest connected component (the one with the highest number of distinct nodes). If there is a tie, pick the component whose nodes contain the lexicographically smallest node name.

4. **Output Generation**:
   Your program must write the results to a file named `/home/user/component_result.txt` with exactly two lines:
   - Line 1: An integer representing the number of nodes in the largest connected component.
   - Line 2: A comma-separated list of the node names in that component, sorted in lexicographical ascending order (e.g., `A,B,D,Z`).

**Requirements**:
- Write your solution in a single C++ file at `/home/user/graph_analyzer.cpp`.
- Compile it using `g++ -O3 -std=c++17 -o /home/user/graph_analyzer /home/user/graph_analyzer.cpp`.
- Execute the compiled program to generate the required `/home/user/component_result.txt` file.
- You may use only the C++ standard library (no external libraries like Boost).