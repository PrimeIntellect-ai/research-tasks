You are helping a researcher organize a dataset of academic collaborations. The researcher is trying to compute the "Erdös number" (shortest path distance in the co-authorship graph) from a specific primary investigator (Author ID: 1) to all other authors in the dataset.

The dataset is stored in an SQLite database at `/home/user/dataset/collaborations.db`.

The researcher wrote a Python script at `/home/user/generate_report.py` that uses a Recursive CTE (Common Table Expression) to traverse the graph and export the distances. However, the script is incredibly slow, consumes massive amounts of memory, and seems to return incorrect, inflated distance results. The researcher suspects there is an implicit cross-join or missing join condition in the recursive step of the query.

Additionally, the researcher has provided a compiled, stripped binary tool at `/app/path_oracle` which computes the true shortest paths using a highly optimized BFS algorithm, but it only accepts raw edge lists and outputs to standard out.

Your task:
1. Reverse engineer the SQLite database schema in `/home/user/dataset/collaborations.db` to understand the table structures.
2. Fix the SQL query inside `/home/user/generate_report.py` to correctly compute the shortest paths (resolving the implicit cross join and any infinite loop issues in the cyclic graph).
3. Ensure the script exports the results to `/home/user/distances.json` in the exact format: `{"<author_id>": <distance>, ...}`. 
4. The optimized script must run efficiently. An automated test will evaluate your script's execution time and accuracy against the reference output from `/app/path_oracle`.

The target performance metric is an execution time of **less than 1.0 second**, and a strictly matching output to the true shortest paths.