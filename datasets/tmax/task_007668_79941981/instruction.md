You are an AI assistant helping a researcher organize their dataset of academic papers. The researcher has extracted a subset of their NoSQL database into a JSONL (JSON Lines) file located at `/home/user/papers.jsonl`.

Your goal is to build a Python data pipeline that chains together document filtering, graph analytics (centrality and clustering), and format conversion to find the most influential papers and their respective research communities.

Please create a Python script that performs the following steps:
1. **NoSQL Document Filtering:** Read `/home/user/papers.jsonl`. Each line is a JSON object with keys: `paper_id` (string), `year` (integer), and `citations` (list of strings representing `paper_id`s of cited papers). Filter the dataset to only include papers published in or after the year 2010.
2. **Graph Construction:** Using the `networkx` library, build a Directed Graph. The nodes ($V$) should be exactly the `paper_id`s of the papers that passed the filter (published >= 2010). Add directed edges for citations (e.g., if Paper A cites Paper B, add an edge from A to B). Ignore any citations to `paper_id`s that do not exist in your filtered set of nodes (i.e., remove edges pointing to pre-2010 or unknown papers).
3. **Graph Analytics - Centrality:** Calculate the PageRank of every node in the graph using `networkx.pagerank(G, alpha=0.85)`.
4. **Graph Analytics - Clustering:** Find the Weakly Connected Components of the graph. Assign a `component_id` to each node. The `component_id` must be the lexicographically smallest `paper_id` string within that component.
5. **Format Conversion & Export:** Export the results to a CSV file located at `/home/user/top_papers.csv`. The CSV must have exactly these columns in order: `paper_id`, `pagerank`, `component_id`. 
   - Round the `pagerank` values to exactly 4 decimal places (e.g., `0.1234`).
   - Sort the rows by `pagerank` in descending order. If there is a tie, sort by `paper_id` in ascending alphabetical order.

You may install `networkx` via `pip` if it is not already installed. Create the Python script and run it to produce the final CSV file.