You are an AI assistant helping a data researcher organize and analyze a complex dataset of academic citations. The data is currently fragmented across two different formats: a document-based JSON file containing paper metadata, and a relational CSV file containing citation links.

Your task is to integrate these datasets into a graph structure, perform specific graph analytics, and export the aggregated results into a precise JSON format.

Here are the details of the datasets:
1. **Metadata Store:** `/home/user/data/papers.json` - A JSON file containing a list of dictionaries. Each dictionary has a `paper_id` (string), `title` (string), and `authors` (list of strings).
2. **Relational Citations:** `/home/user/data/citations.csv` - A CSV file with two columns: `source_id` and `target_id`. Each row represents a citation where the `source_id` paper cites the `target_id` paper.

Your objectives:
1. Install any necessary Python libraries (e.g., `networkx` is highly recommended).
2. Write a Python script to read the datasets and construct a **Directed Graph**. An edge should exist from `source_id` to `target_id` (meaning the source cites the target). Ensure all `paper_id`s from the JSON are added as nodes, even if they have no citations.
3. **Graph Analytics - Centrality:** Calculate the PageRank of every paper in the directed graph using an alpha parameter of `0.85` (default in NetworkX). Identify the top 5 papers with the highest PageRank scores. If there is a tie in scores, resolve it by sorting the `paper_id`s alphabetically.
4. **Graph Analytics - Clustering:** Convert the graph to an **undirected graph** (treating all edges as bidirectional and removing duplicates/self-loops). Then, use the greedy modularity maximization algorithm (specifically `networkx.algorithms.community.greedy_modularity_communities`) to find communities within the network. Calculate the sizes of all resulting communities.
5. **Format Conversion & Export:** Create a results file at `/home/user/graph_results.json` containing exactly the following structure:
   ```json
   {
     "top_5_pagerank": ["id1", "id2", "id3", "id4", "id5"],
     "top_3_community_sizes": [size1, size2, size3]
   }
   ```
   *Note: `top_3_community_sizes` should be a list of integers representing the sizes of the three largest communities, sorted in descending order.*

You may create any intermediate scripts you need. Ensure your final output exactly matches the requested JSON schema.