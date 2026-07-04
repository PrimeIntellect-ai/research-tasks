You are a data analyst working with a custom graph dataset. We have a pipeline that extracts transaction edges into a CSV format, and we need to run complex 2-hop queries on this graph to detect suspicious transaction chains.

Currently, doing this with standard tools like pandas is too slow and uses too much memory for our production environment. Your task is to write a highly optimized C program that processes these queries by designing an efficient internal index strategy (like a Compressed Sparse Row or adjacency list) and optimizing the query execution plan.

Here are the details:
1. **Inputs:**
   - Graph data: `/home/user/data/edges.csv`
     - Format: `source_node,target_node,weight`
     - Types: `uint32_t`, `uint32_t`, `float`
     - Represents directed edges. A node can have multiple outgoing edges.
   - Queries: `/home/user/data/queries.csv`
     - Format: `start_node,min_weight_sum`
     - Types: `uint32_t`, `float`

2. **The Query:**
   For each query `(start_node, min_weight_sum)` in `queries.csv`, you need to find the number of *distinct* destination nodes `C` such that there exists a valid 2-hop path `start_node -> B -> C` where:
   - `start_node != B` and `B != C` and `start_node != C` (no self-loops or cycles in the 2-hop path)
   - `weight(start_node -> B) + weight(B -> C) >= min_weight_sum`

3. **Requirements:**
   - Write your solution in C at `/home/user/graph_query.c`.
   - Compile it to `/home/user/graph_query` using `gcc -O3 graph_query.c -o graph_query`.
   - The program must take no arguments and read directly from `/home/user/data/edges.csv` and `/home/user/data/queries.csv`.
   - The program must output the results to `/home/user/results.csv`.
   - Output format: `start_node,min_weight_sum,count` (where `min_weight_sum` is printed with exactly 2 decimal places, e.g., `%.2f`).
   - Performance matters. A naive O(E^2) loop will time out. You must design a proper index (e.g., adjacency list) in C to achieve efficient O(degree) lookups.

Ensure your program executes successfully and generates the correct `/home/user/results.csv`.