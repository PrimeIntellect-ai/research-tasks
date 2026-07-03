You are a bioinformatics researcher modeling molecular interaction networks. You have a set of simulated network graphs and want to compare the distribution of specific path lengths in these networks against an empirical reference dataset.

Your task is to write a Rust program that computes the Total Variation Distance (TVD) between the simulated shortest-path distributions and the reference distribution.

Here are the specifications:

1. **Input Data**:
   - Directory `/home/user/networks/` contains two text files (`graph_1.txt`, `graph_2.txt`). Each file is an undirected graph represented as a space-separated edge list (one edge per line: `node_u node_v`).
   - File `/home/user/node_types.csv` contains the type assignment for each node (header: `node_id,type`). Types are 'A', 'B', or 'C'.
   - File `/home/user/reference_dist.json` contains the reference probability distribution of shortest path lengths. The keys are string representations of the path length (number of edges), and the values are the probabilities (floats).

2. **Simulation Metric**:
   - For *each* graph, find all pairs of nodes $(u, v)$ where $u$ has type 'A' and $v$ has type 'B'.
   - Compute the shortest path length (minimum number of edges) between $u$ and $v$. If there is no valid path between $u$ and $v$ in the graph, ignore that pair.
   - Aggregate all these finite shortest path lengths across *all* graphs in the directory into a single combined dataset.
   - Calculate the empirical probability distribution of these path lengths (i.e., the frequency of each path length divided by the total number of valid A-B paths found across all graphs).

3. **Comparison (Total Variation Distance)**:
   - Compute the Total Variation Distance between your simulated distribution ($P_{sim}$) and the reference distribution ($P_{ref}$).
   - The formula for TVD between two discrete probability distributions is:
     $TVD = 0.5 \times \sum_{k} |P_{sim}(k) - P_{ref}(k)|$
     where $k$ ranges over all path lengths present in *either* distribution. Treat the probability of a missing path length in either distribution as `0.0`.

4. **Output**:
   - Write a Rust project in `/home/user/graph_compare` to perform this analysis.
   - The Rust program must output the final TVD value formatted to exactly 4 decimal places (e.g., `0.1234`) and write it to `/home/user/tvd_result.txt`. Do not include any other text in this file.

Use standard Rust tools (`cargo`) to create and build your project. You can use standard libraries or popular crates (like `petgraph`, `serde_json`, `csv`) as needed.