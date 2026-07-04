I am a data analyst working with some network communication data, and I've been running into trouble. I have two files: `/home/user/nodes.csv` and `/home/user/edges.csv`. 

Earlier, I wrote a SQL query to extract some graph metrics, but I made a mistake and implicitly cross-joined the tables, which completely inflated all my byte counts and degree metrics. I need you to write a script in the language of your choice (Python, bash, etc., or load it into a local SQLite DB) to compute the correct metrics from scratch and output them to a new CSV.

Please compute the following metrics for each node present in `nodes.csv`:
1. `out_degree`: The number of distinct destination nodes (`dst`) this node sends data to. (If a node sends nothing, out_degree is 0).
2. `total_bytes`: The total sum of `bytes` sent by this node (as `src`). (If none, total_bytes is 0).
3. `rank`: The dense rank of the node based on `out_degree` (descending). If there is a tie, break the tie using `total_bytes` (descending), and if still tied, break it by `node_id` (alphabetically ascending). The highest out_degree should have rank 1.
4. `cumulative_bytes`: A rolling sum (window function style) of `total_bytes` ordered by the `rank` calculated in step 3. 

Output the results to exactly `/home/user/graph_stats.csv`. 
The file must be a standard CSV with the exact following header:
`node_id,department,out_degree,total_bytes,rank,cumulative_bytes`

Ensure that the rows in the output CSV are ordered by `rank` ascending.