You are a Database Administrator optimizing a complex knowledge graph database. You have received a screenshot of the latest query execution plan's topology, which details the join costs between different NoSQL collections (nodes). This image is located at `/app/schema_graph.png`.

The image contains a simple text representation of an undirected edge list, formatted as:
`NodeA NodeB Cost`

Your task is to identify the "bottleneck" collections by calculating the exact Closeness Centrality for every node in the graph extracted from the image. 

1. Inspect the image `/app/schema_graph.png` and extract the graph topology and join costs (edge weights). You may use OCR tools like `tesseract` which are available on the system.
2. Write a C program at `/home/user/analyze_graph.c` that:
   - Hardcodes or reads the extracted graph structure.
   - Computes the shortest path between all pairs of nodes (using the join costs as distance weights).
   - Calculates the closeness centrality for each node using the formula: $C(u) = \frac{N-1}{\sum_{v \neq u} d(u,v)}$ where $N$ is the total number of nodes, and $d(u,v)$ is the shortest path distance between node $u$ and node $v$.
3. Compile and execute your C program.
4. Output the calculated centralities to `/home/user/centralities.txt`. Each line should be formatted exactly as `NodeName: 0.XXXX` (rounded to 4 decimal places), sorted alphabetically by NodeName.

An automated verifier will read `/home/user/centralities.txt` and compute the Mean Squared Error (MSE) between your centralities and the true centralities. Your MSE must be less than 0.001 to pass.