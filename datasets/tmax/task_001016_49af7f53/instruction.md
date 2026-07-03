You are helping a computational researcher organize a large hierarchical taxonomy dataset. We have an SQLite database at `/home/user/taxonomy.db` representing a graph of categories and subcategories. 

The database has two tables:
1. `nodes(id INTEGER PRIMARY KEY, category_group TEXT)`
2. `edges(parent_id INTEGER, child_id INTEGER, weight REAL)`

We have a legacy compiled tool located at `/app/legacy_calc` that calculates the top 3 most "influential" nodes within each `category_group`. Influence is defined as the total sum of the `weight` of all edges in the entire subtree rooted at a given node (i.e., its direct children, their children, and so on). The tool ranks them and outputs the top 3 per group.

Unfortunately, `/app/legacy_calc` is extremely slow. We need you to write a high-performance C program that achieves the exact same result but significantly faster.

Your task:
1. Write a C program at `/home/user/fast_graph.c` that connects to `/home/user/taxonomy.db` using the SQLite3 C API.
2. Your program must calculate the exact same metric as the legacy tool: the total descendant weight for all nodes, ranked within their `category_group`.
3. Filter the results to only include the top 3 nodes per `category_group` (rank 1 to 3).
4. Output the results to `/home/user/results.csv` in the exact format: `category_group,id,total_weight,rank`.
5. Your solution must run significantly faster than the legacy tool. You are encouraged to design and execute database indexing strategies, and utilize advanced SQL capabilities like recursive hierarchical queries and window functions directly within your C program's queries.
6. Compile your program to `/home/user/fast_graph` (ensure you link `sqlite3`).

You can run `/app/legacy_calc` (it takes no arguments and reads from `/home/user/taxonomy.db`, outputting to standard output) to inspect its exact output format and behavior.