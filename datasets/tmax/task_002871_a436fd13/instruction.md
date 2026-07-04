We have a proprietary query engine compiled as a stripped binary at `/app/graph_oracle`. This tool takes an edge list in CSV format and outputs analytical metrics for each node in the graph. As a database administrator optimizing our graph pipelines, you need to replace this slow binary with a highly optimized C++ implementation.

Your task:
1. Examine `/app/graph_oracle`. It takes two arguments: an input CSV file and an output CSV file (e.g., `/app/graph_oracle input.csv output.csv`). 
2. Figure out the exact analytical aggregations and window-like ranking logic the oracle is applying to the graph nodes. (Hint: it involves connected components, node degrees, and ranking within those components).
3. Write a C++ program at `/home/user/fast_graph.cpp` that exactly replicates the oracle's output logic but runs significantly faster.
4. Compile your program to `/home/user/fast_graph`. It must accept the same two command-line arguments (input file, output file) and produce identical output to the oracle.

The input CSV contains two columns: `source,target` (undirected edges).
The output CSV must contain four columns: `node,component_id,degree,rank`. Nodes should be sorted by `node` ascending.

Your compiled program `/home/user/fast_graph` will be tested against a massive, 5-million edge hidden dataset. It must produce the exact same output as `/app/graph_oracle` but run in under 2.0 seconds. 

Please create a `Makefile` or just ensure `g++ -O3 /home/user/fast_graph.cpp -o /home/user/fast_graph` works.