As a database administrator optimizing our graph analytics pipeline, you've been tasked with replacing an old, extremely slow legacy tool. 

We have a stripped binary located at `/app/graph_oracle` that computes a specific centrality score for nodes in a directed graph. Unfortunately, the source code and the original Cypher/SPARQL queries used to design it have been lost. We know it computes some form of centrality (like PageRank, Closeness, or Betweenness) but with specific, non-standard parameters. 

Your task:
1. Reverse-engineer the data model and the exact centrality algorithm/parameters the binary is using by feeding it small, custom edge-list graphs.
2. Write a highly optimized, functionally equivalent program or script. You must provide an entrypoint script at `/home/user/fast_centrality.sh`.
3. Your script must accept exactly two arguments, identical to the legacy binary:
   `./fast_centrality.sh <input_edgelist.txt> <output_scores.txt>`

Input format: A tab-separated file with two columns indicating a directed edge: `source_node \t target_node` (nodes are integers).
Output format: A tab-separated file with two columns: `node_id \t score` (scores rounded to 6 decimal places), sorted by `node_id` ascending.

Your solution must produce outputs with a Mean Squared Error (MSE) of less than 0.0001 compared to the oracle, but it must run significantly faster. We will test your script on a large graph to measure its execution speedup.