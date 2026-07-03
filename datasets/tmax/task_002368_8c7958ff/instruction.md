You are acting as a Database Administrator for a high-performance analytics system. We have a custom in-memory graph engine written in C that evaluates reachability and shortest paths between users and products. Currently, our system reads a relational edge list and evaluates shortest paths using a naive, highly unoptimized approach, causing query timeouts.

Your task is to write a highly optimized C program from scratch to replace the legacy engine. You must process a dataset, build an efficient index, execute a set of shortest path queries, and apply filtering, sorting, and pagination.

**System Requirements & Input Data:**
1. **Edge Data:** `/home/user/data/edges.csv`
   Format: `source_node,target_node,weight` (comma-separated, no header).
   This represents a directed graph. Node IDs are integers from 0 to 9999. Weights are positive integers.
2. **Query Data:** `/home/user/data/queries.csv`
   Format: `source_node,target_node` (comma-separated, no header).
   Contains pairs of nodes for which you must find the shortest path distance.

**Functional Requirements:**
1. **Index Strategy & Cross-Representation:** The input is relational (CSV). You must parse this into an efficient in-memory Graph representation (e.g., an Adjacency List) to optimize traversal.
2. **Graph Traversal:** For every pair in `queries.csv`, compute the shortest path distance from `source_node` to `target_node`. If no path exists, the distance is considered infinite.
3. **Filtering:** Discard any query results where no path exists, or where the shortest path distance is **strictly greater than 5000**.
4. **Sorting:** Sort the filtered results primarily by `distance` (ascending). In case of ties, sort by `source_node` (ascending). If still tied, sort by `target_node` (ascending).
5. **Pagination:** Apply pagination to the sorted results. Skip the first 10 results (OFFSET = 10) and take the next 20 results (LIMIT = 20). 
6. **Output:** Write the final paginated results to `/home/user/result.csv`.
   Format: `source_node,target_node,distance` (comma-separated, no header, exactly 20 lines assuming there are enough results).

**Constraints & Guidelines:**
- Write your C program in `/home/user/graph_optimizer.c`.
- You may only use standard C libraries (e.g., `stdio.h`, `stdlib.h`, `limits.h`). Do not use external libraries for the graph algorithms.
- Compile your code using `gcc -O3 /home/user/graph_optimizer.c -o /home/user/graph_optimizer`.
- Execute your program and ensure `/home/user/result.csv` is correctly populated.
- The entire C program execution should take less than 2 seconds.