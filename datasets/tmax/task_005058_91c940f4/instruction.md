You are an AI assistant helping a data researcher organize and analyze a massive dataset of paper citations. The citations form a directed knowledge graph.

We have a vendored local package called `sh-graph-tools` located at `/app/sh-graph-tools` that provides basic graph traversal utilities. However, the package is currently broken:
1. The `Makefile` fails to install the scripts properly (it crashes when you run `make install` due to a syntax error).
2. The core script `src/dfs.sh`, which calculates all reachable nodes from a given starting node in a directed graph, has a bug where it gets stuck in an infinite loop if the graph contains cycles.

Your task has two parts:

**Part 1: Fix the Vendored Package**
- Navigate to `/app/sh-graph-tools`.
- Fix the `Makefile` so that `make install` successfully copies the scripts to `/app/sh-graph-tools/bin` and makes them executable.
- Fix the bug in `src/dfs.sh` so that it correctly tracks visited nodes and gracefully handles cyclic graphs without infinitely looping.

**Part 2: Create the Graph Analyzer Script**
Write a bash script at `/home/user/graph_analyzer.sh` that uses the fixed tools (or your own logic) to perform a hierarchical query and graph analytics. 

The script must accept exactly two arguments:
`./graph_analyzer.sh <input_edge_file> <start_node>`

The `<input_edge_file>` is a space-separated text file where each line represents a directed edge (e.g., `PaperA PaperB`, meaning Paper A cites Paper B).

Your script must:
1. Find all nodes reachable from the `<start_node>` (including the start node itself).
2. Calculate the "in-degree" (number of incoming edges from the ENTIRE graph) for each of these reachable nodes.
3. Sort the reachable nodes by their in-degree in descending order. If there's a tie, sort them alphabetically by node name (ascending).
4. Filter and paginate the results to output ONLY the top 10 nodes.
5. The output format MUST be exactly:
   `Node: <NodeName>, InDegree: <Degree>`
   (One per line)

Your script must be robust and will be heavily tested against random graphs of varying sizes. Make sure `/home/user/graph_analyzer.sh` is executable.