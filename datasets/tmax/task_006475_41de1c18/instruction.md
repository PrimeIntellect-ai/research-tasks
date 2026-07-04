You are an AI assistant helping a researcher organize and analyze a complex dataset of academic papers. 

The researcher has provided a raw NoSQL-style data dump in JSONL (JSON Lines) format at `/home/user/dataset/papers.jsonl`. Each line contains a JSON object representing a paper, with the following schema:
- `id` (string): Unique identifier for the paper.
- `title` (string): The title of the paper.
- `authors` (list of strings): List of author names.
- `citations` (list of strings): List of `id`s of other papers that this paper cites.
- `keywords` (list of strings): Keywords associated with the paper.

Your task is to perform the following steps to analyze the citation network:

1. **Graph Materialization & Database Setup**: 
   Write a Python script that reads the JSONL file and loads it into a local SQLite database at `/home/user/research.db`. You must design a schema that properly normalizes this document-oriented data into relational tables (e.g., `papers`, `paper_authors`, `paper_citations`, `paper_keywords`).

2. **Graph Analytics**:
   Query your SQLite database to extract the citation network. Using Python (e.g., the `networkx` library), build a directed graph where an edge from node $A$ to node $B$ means paper $A$ cites paper $B$. 
   Calculate the PageRank centrality for all nodes in the graph using the standard parameters (alpha=0.85).

3. **Complex Filtering & Output**:
   The researcher is specifically interested in the "machine_learning" keyword cluster. Filter the calculated PageRank results to include ONLY papers that have the keyword "machine_learning". 
   Find the top 3 papers in this cluster sorted by their PageRank in descending order. If there is a tie, sort by `id` in ascending order.
   
   Output these top 3 papers to a CSV file at `/home/user/influential_ml_papers.csv`.
   The CSV must have the exact header: `id,title,pagerank`
   The `pagerank` values must be rounded to exactly 4 decimal places.

Ensure your code handles dependencies appropriately (you may install packages using `pip`).