I need your help organizing and analyzing a citation network dataset I've been working on. I have a SQLite database at `/home/user/citation_data.db` containing two tables: `papers` (id, year, venue) and `citations` (source_id, target_id). 

I also have an old scanned diagram at `/app/weight_params.png` that contains the specific weighting rules for our graph analytics pipeline. You'll need to read the parameters from that image. The image contains a table specifying the "Decay Factor" for different years and the "Damping Factor" for the PageRank algorithm.

Here is what I need you to do:
1. Extract the parameters from the image `/app/weight_params.png`.
2. Write a bash script `extract_subgraph.sh` that uses a complex SQL query to extract a subgraph from `/home/user/citation_data.db`. The query must use window functions to keep only the top 5 most recently published outgoing citations for each paper (based on the target paper's publication year). Output this to `subgraph.csv`.
3. Chain this output into a Python script `compute_centrality.py` that builds a directed graph, applies the decay weights based on the year difference between the source and target papers (using the rules from the image), and computes the weighted PageRank for all nodes.
4. Save the final output as a CSV at `/home/user/pagerank_results.csv` with columns `node_id` and `pagerank_score`.

Your final output will be graded based on the Mean Squared Error (MSE) of your PageRank scores compared to our golden reference set. Ensure your pipeline is fully automated and runs correctly.