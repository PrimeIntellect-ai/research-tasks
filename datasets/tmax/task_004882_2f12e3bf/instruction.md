You are an AI assistant helping a researcher organize a dataset of academic citations. The researcher has provided a raw CSV dataset of citation edges and needs you to perform a series of graph operations to analyze the hierarchical structure of the citations.

Your task is to write and execute a Python script (`/home/user/analyze_citations.py`) that processes the dataset and extracts specific graph analytics. 

Here are the step-by-step requirements:
1. **Setup**: Install any necessary Python packages (like `networkx`).
2. **Data Loading**: Read the citation dataset located at `/home/user/citations.csv`. The file has a header `source,target` where each row represents a directed edge meaning `source` paper cites `target` paper. Load this into a directed graph.
3. **Graph Analytics**: Compute the PageRank of all nodes in the graph using the default damping factor (0.85). Identify the "Top Paper" (the node with the highest PageRank score).
4. **Hierarchical Query**: Compute the longest path (maximum number of edges) from any paper in the graph *to* the Top Paper. This represents the maximum depth of the citation tree leading to the most influential paper.
5. **Graph Projection and Export**: Create a subgraph containing the Top Paper and all of its ancestors (papers that cite the Top Paper directly or indirectly). Export this subgraph to a GraphML file at `/home/user/top_paper_subgraph.graphml`.
6. **Summary Report**: Output the analytical results to a JSON file at `/home/user/summary.json` with the following strict structure:
```json
{
  "top_paper_id": 7,
  "pagerank_score": 0.1234, 
  "max_depth_to_top": 5
}
```
*Note: The `top_paper_id` should be an integer, `pagerank_score` should be a float rounded to exactly 4 decimal places, and `max_depth_to_top` should be an integer representing the number of edges in the longest path.*

The raw dataset `/home/user/citations.csv` is already present on the system. You must write the script, run it, and ensure the `summary.json` and `top_paper_subgraph.graphml` files are generated perfectly.