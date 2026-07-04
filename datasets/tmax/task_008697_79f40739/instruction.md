I am a researcher organizing a messy dataset of academic papers and authors. I have a custom SQLite database located at `/home/user/research_data.db` that contains a generic graph representation of my dataset. 

I need you to extract this data, map it into a proper graph network, perform some analytics, and summarize the research communities.

Here is what you need to do:
1. **Reverse Engineer the Data Model:** Inspect `/home/user/research_data.db`. It contains generic `nodes` and `edges` tables. Nodes have a JSON `properties` column and a `label` (e.g., 'Author', 'Paper'). Edges have a `type` (e.g., 'WROTE', 'CITES').
2. **Cross-Representation Mapping:** Construct a directed "Author Citation Graph". In this new graph, the nodes are Authors. A directed edge from Author A to Author B exists if Author A 'WROTE' a paper that 'CITES' a paper that Author B 'WROTE'. Ensure this is a simple directed graph (no parallel edges between the same two authors, even if there are multiple citations).
3. **Graph Analytics:** 
   - Identify the distinct research communities by calculating the **Weakly Connected Components** of the Author Citation Graph.
   - Calculate the **PageRank** (using standard NetworkX `pagerank` defaults: alpha=0.85) for all authors in the Author Citation Graph to determine their influence.
4. **Aggregation and Summarization:** For each community (component), determine its size (number of authors) and identify its most influential author (the author with the highest PageRank score within that component). If there is a tie in PageRank, choose the author with the lowest numerical ID.

Output the final summarized results to a JSON file at `/home/user/author_summary.json`. 
The JSON must be a list of dictionaries, sorted by community size in descending order (and then by the top author's ID in ascending order if sizes tie).
Each dictionary must exactly match this format:
```json
[
  {
    "community_size": 4,
    "top_author_id": 1,
    "top_author_name": "Dr. Alice"
  },
  ...
]
```
Ensure your code is reproducible and all operations are run in the `/home/user` directory.