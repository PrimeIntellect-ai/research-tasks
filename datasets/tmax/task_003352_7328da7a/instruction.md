You are a data engineer building ETL pipelines. We have extracted a dependency graph of our pipeline jobs, represented as directed edges between job IDs. We need to identify the most critical upstream jobs that trigger many other jobs (high out-degree centrality) so we can prioritize their optimization.

Your task is to write a C program that performs this graph analysis, sorts, filters, and paginates the results efficiently.

1. There is a file at `/home/user/etl_edges.txt`. Each line contains two space-separated integers, `SOURCE` and `TARGET` (1 <= ID <= 50000), representing a directed edge `SOURCE -> TARGET`.
2. Write a C program at `/home/user/graph_analyzer.c` and compile it to `/home/user/graph_analyzer`.
3. The program must accept exactly 4 command-line arguments:
   `./graph_analyzer <filepath> <MIN_DEGREE> <OFFSET> <PAGE_SIZE>`
4. The program should use a direct-access array (an in-memory index strategy) to efficiently calculate the out-degree (number of outgoing edges) for every node ID present in the file.
5. Filter the nodes to only include those with an out-degree `>= MIN_DEGREE`.
6. Sort the filtered nodes in **descending order of out-degree**. For nodes with the same out-degree, resolve ties by sorting in **ascending order of their Node ID**.
7. Paginate the sorted results: skip the first `OFFSET` nodes, and output up to `PAGE_SIZE` nodes.
8. The program must write the paginated results to `/home/user/critical_nodes.log`.
   Each line must be formatted exactly as: `NodeID: OutDegree`

Please write the program, compile it, and run it with the following parameters:
`./graph_analyzer /home/user/etl_edges.txt 10 5 10`

(Note: Do not install any external libraries, use standard C libraries only).