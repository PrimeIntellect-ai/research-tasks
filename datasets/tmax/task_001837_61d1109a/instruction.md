I am a researcher organizing a large, complex dataset of academic papers, authors, and citations. Currently, the dataset is fragmented across different formats:
- `/home/user/data/authors.csv`: Relational data containing author IDs, names, and institutional affiliations.
- `/home/user/data/papers/`: A directory containing thousands of JSON documents. Each document represents a paper, including its ID, title, full text, and an array of referenced paper IDs.

I have a legacy, compiled tool located at `/app/citation_oracle` (a stripped binary). This tool takes three arguments: the path to the `authors.csv`, the `papers` directory, and a file containing a batch of queries `/home/user/queries.txt`. For each query (an author ID), it computes a proprietary "Influence Score" based on a multi-hop citation graph traversal, filtering and paginating the results internally, and outputs a JSON file with the scores.

Unfortunately, `/app/citation_oracle` is extremely slow and lacks proper indexing, making it unusable for my full dataset. 

Your task is to:
1. Reverse-engineer the algorithmic logic of the `/app/citation_oracle` by treating it as a black box (or inspecting it). 
2. Write an optimized implementation to compute the exact same "Influence Score" for any given author ID. You may use any combination of Python, a local database service (like PostgreSQL or SQLite, which you must configure), or other tools.
3. Design and implement a robust indexing strategy (e.g., building materialized views, inverted indices, or in-memory graph structures) so your implementation runs significantly faster than the oracle.
4. Your final solution must be a script located at `/home/user/fast_oracle.py` (or a similar executable wrapper) that takes the same inputs (`authors.csv`, `papers` dir, `queries.txt`) and outputs the results to `/home/user/fast_results.json` in the exact same format as the binary oracle.

Success will be measured by the correctness of your output compared to the oracle and the execution speedup. Your solution must achieve at least a 10x speedup over the binary oracle when run on a held-out test set of 1000 queries.