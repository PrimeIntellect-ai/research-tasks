You are a data engineer building ETL pipelines. We have a C program, `/home/user/graph_etl.c`, designed to act as a custom query engine. It reads a list of graph edges from `/home/user/edges.txt`, constructs an adjacency matrix, computes the shortest path from a starting node using Dijkstra's algorithm, and outputs the results.

However, the previous developer introduced a logical flaw akin to an "implicit cross join" in SQL. When mapping the text-based edges to the internal adjacency matrix, the loop structure accidentally connects the source node of an edge to *every* other node in the graph with that edge's weight, rather than just the target node. This results in completely incorrect path distances.

Your task:
1. Identify and fix the "implicit cross join" bug in `/home/user/graph_etl.c` so that edges are only created between the specific 'From' and 'To' nodes defined in the input file.
2. Compile the fixed C program.
3. Run the program using `/home/user/edges.txt` as the input dataset and `A` as the starting node.
4. Export the output to a file located at `/home/user/output.tsv`. 
5. The final `/home/user/output.tsv` must contain tab-separated values (`Node\tDistance`), sorted first by `Distance` (numerically, ascending), and then by `Node` name (alphabetically, ascending). You may use standard shell tools (like `sort`) to format the output of your C program into the final file.

The program should print paths to reachable nodes only.