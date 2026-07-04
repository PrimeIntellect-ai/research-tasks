I am a researcher organizing a massive dataset of academic citations. As part of our data comprehension pipeline, we rely on a custom "Influence Centrality" metric to identify key papers. 

We have a legacy tool, provided as a stripped binary at `/app/graph_oracle.bin`, that computes this metric. It executes a hardcoded, unoptimized graph traversal query to calculate the centrality score of a given node. Unfortunately, because we don't have the source code, we cannot optimize its query plan, and it's too slow for our multi-terabyte datasets.

I need you to:
1. Treat `/app/graph_oracle.bin` as a black box. Experiment with it by creating small test edge lists to deduce the exact graph analytic formula (the implicit graph query) it computes.
2. Write a highly optimized C++ replacement in `/home/user/solution.cpp`.
3. Compile your code to an executable at `/home/user/solution`.

**Executable Interface:**
Both the oracle and your solution must accept exactly two positional arguments:
`./executable_name <path_to_edgelist_file> <target_node_id>`

- `<path_to_edgelist_file>`: A text file where each line contains two space-separated integers `U V`, representing a directed edge from node `U` to node `V` (e.g., paper U cites paper V).
- `<target_node_id>`: An integer ID of the node whose influence centrality score is being calculated.
- The program must print only the integer score to standard output, followed by a newline.

Your C++ implementation must be bit-exact equivalent to the oracle's output for any valid directed graph and target node. You should compile it using standard `g++` (e.g., `g++ -O3 /home/user/solution.cpp -o /home/user/solution`).

Use the tools available in your terminal to create graphs, probe the binary, deduce the graph centrality algorithm, and implement your C++ solution.