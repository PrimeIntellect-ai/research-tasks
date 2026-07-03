You are helping a researcher organize and analyze a large directed citation network dataset. 

The researcher has been using a legacy tool located at `/app/citation_oracle` to find the shortest path distance between papers in the network. This stripped binary takes three arguments: an edgelist file, a source node ID, and a target node ID (e.g., `/app/citation_oracle graph.txt 10 42`). It correctly outputs the integer shortest path length (or -1 if no path exists). However, it is extremely slow, as it re-parses the graph for every single query and uses an inefficient traversal algorithm.

Your task is to write a highly optimized Bash script at `/home/user/fast_query.sh` that can process a batch of queries much faster. 
Your script will be invoked as:
`/home/user/fast_query.sh <edgelist_file> <queries_file>`

- `<edgelist_file>` contains space-separated integers representing directed edges (`source target`).
- `<queries_file>` contains space-separated integers representing queries (`source target`), one per line.
- Your script must output the shortest path distance for each query to `stdout`, one per line, matching the exact order of the queries. Output `-1` if no path exists.

To achieve the required performance, your Bash script should leverage `sqlite3`. You will need to write commands within your script to:
1. Initialize an in-memory or temporary SQLite database.
2. Load the edgelist data.
3. Construct appropriate indexes to optimize the query plan.
4. Execute parameterized recursive Common Table Expressions (CTEs) to compute the shortest paths for the provided pairs.

The automated test will evaluate your script's accuracy against the oracle and measure its total execution time for a large batch of queries. You must achieve a substantial speedup to pass the performance threshold.