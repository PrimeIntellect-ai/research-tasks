You are a data analyst working with a custom social network dataset. We have a massive graph dataset exported as a CSV file located at `/home/user/data/edges.csv`. 

The CSV has the following format:
`source_node_id,target_node_id,base_weight,properties_json`

For example:
`10,42,5.0,{"type":"friend","penalty":1.5}`

The effective traversal cost (weight) of an edge is dynamically calculated using a NoSQL-style aggregation logic:
`effective_weight = base_weight * properties_json["penalty"]`

We have a proprietary query engine provided as a stripped binary at `/app/graph_oracle`. It takes a CSV file and a file containing pairs of nodes to query, and computes the shortest path cost between each pair based on the effective weight.
Usage: `/app/graph_oracle /home/user/data/edges.csv /home/user/data/queries.txt`

The problem is that `/app/graph_oracle` is incredibly slow for batch queries. It appears to linearly scan and re-parse the JSON properties for every single query without any indexing or caching.

Your task is to write a highly optimized C program at `/home/user/fast_path.c` that performs the exact same operation but much faster.
1. Your program should compile to `/home/user/fast_path` (e.g., using `gcc -O3 /home/user/fast_path.c -o /home/user/fast_path -lm`).
2. It must accept two arguments exactly like the oracle: `<csv_path>` and `<queries_txt_path>`.
3. It must output the shortest path cost for each query pair in `<queries_txt_path>`, one float per line (formatted to 2 decimal places, e.g., `12.50`), to standard output. If no path exists, output `-1.00`.
4. You should implement an efficient index strategy (e.g., parsing the CSV once and building an in-memory adjacency list) and use an efficient graph traversal algorithm (like Dijkstra's algorithm) to compute the shortest paths.
5. You must write your own JSON parsing logic or use standard C string functions to extract the `penalty` value from the `properties_json` string.

We will test your program against a held-out dataset and a massive queries file. Your solution will be evaluated based on its correctness (it must exactly match the output of `/app/graph_oracle`) and its performance. You must achieve a speedup of at least 50x compared to the oracle.