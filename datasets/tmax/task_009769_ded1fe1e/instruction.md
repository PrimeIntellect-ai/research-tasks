You are a data analyst investigating potential conflicts of interest and corporate influence within a network of companies and executives. 

You have been given two CSV files in the `/home/user/data/` directory representing a corporate knowledge graph:
1. `nodes.csv` - Contains columns: `id`, `label` (e.g., 'Person', 'Company'), `name`
2. `edges.csv` - Contains columns: `source` (node id), `target` (node id), `type` (e.g., 'CEO_of', 'sits_on_board', 'invested_in')

Your task is to write a Python script (or scripts) to analyze this data and produce two output files. You may install standard data science libraries like `pandas` and `networkx` via pip if needed.

**Objective 1: Knowledge Graph Pattern Matching**
We need to find a specific "conflict of interest" pattern. Find all `Person` nodes that satisfy the following exact structural pattern:
- The Person is `CEO_of` Company X.
- The same Person `sits_on_board` of Company Y.
- Company Y `invested_in` Company X.

Extract the `name` of every Person who matches this pattern. Write these names to `/home/user/conflict_of_interest.txt`, one name per line, sorted alphabetically.

**Objective 2: Graph Analytics (Centrality)**
Calculate the PageRank of all nodes in the entire network to determine the most influential entities. 
- Treat the graph as directed. 
- Use standard PageRank settings (e.g., NetworkX's `pagerank` with `alpha=0.85`).
- Output the `name` of the top 3 nodes with the highest PageRank score. Write them to `/home/user/top_nodes.txt`, one name per line, sorted from highest PageRank to lowest. (In case of a tie in PageRank, sort alphabetically).

**Deliverables:**
Ensure both `/home/user/conflict_of_interest.txt` and `/home/user/top_nodes.txt` are created with the exact specifications above.