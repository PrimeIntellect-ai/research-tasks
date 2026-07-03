You are acting as a Database Administrator optimizing a slow graph database query. To cut costs and improve performance, we are replacing a heavy NoSQL graph aggregation pipeline with a lightweight, chained pipeline utilizing standard shell tools and a high-performance C executable.

Your task is to build this new query pipeline. 

First, write a C program at `/home/user/project_subgraph.c` that performs graph projection and materialization. 
The program must:
1. Read a directed edge list from standard input (`stdin`). The input format will be CSV, where each line represents an edge: `source_node,target_node` (both are positive integers). 
2. Accept two parameterized CLI arguments: `--root <node_id>` and `--depth <k>`.
3. Materialize the subgraph by finding all distinct nodes reachable from the `<node_id>` within `<k>` hops. (A depth of 0 means only the root node itself. Depth 1 means the root and its immediate neighbors).
4. Print the resulting node IDs to standard output (`stdout`), one per line, sorted in ascending numerical order.

Second, write a shell script at `/home/user/query_pipeline.sh` that chains a data filtering step with your C program.
The script must:
1. Accept exactly three arguments: `root_node`, `depth`, and `min_weight`.
2. Read the raw dataset located at `/home/user/raw_edges.csv`. This file has the format `source,target,weight`.
3. Act as an aggregation pipeline by first using standard shell tools (like `awk` or `grep`) to filter out any edges from `raw_edges.csv` where `weight` is strictly less than `min_weight`.
4. Strip the `weight` column from the filtered results so only `source,target` remains.
5. Pipe this cleaned, filtered data into your compiled C program (which should be compiled to `/home/user/project_subgraph`), passing the `root_node` and `depth` as arguments.

**Constraints & Details:**
* The graph might contain cycles. Your C program must handle this without infinite looping.
* You can assume node IDs are integers between 1 and 100,000.
* You can assume the graph has at most 500,000 edges.
* Do not use any external C libraries beyond the standard library (e.g., `<stdio.h>`, `<stdlib.h>`, etc.).
* Compile your C program using: `gcc -O3 /home/user/project_subgraph.c -o /home/user/project_subgraph`
* Ensure your shell script is executable (`chmod +x /home/user/query_pipeline.sh`).

For testing, I will run your pipeline like this:
`/home/user/query_pipeline.sh 10 3 50 > /home/user/query_result.txt`
This should find all nodes within 3 hops of node 10, traversing only edges with a weight of 50 or more.