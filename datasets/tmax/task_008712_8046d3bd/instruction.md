I am a researcher organizing a dataset of academic papers and their citations. The data is stored as a Knowledge Graph in an SQLite database located at `/home/user/knowledge_graph.db`. 

The database has two tables:
- `papers`: `id` (INTEGER), `title` (TEXT), `year` (INTEGER)
- `citations`: `source` (INTEGER), `target` (INTEGER) representing a directed citation from the `source` paper to the `target` paper.

I need you to write a Python script that does the following:
1. Computes the PageRank centrality of all papers in the citation graph. You can use the `networkx` library to build the directed graph from the `citations` table and compute the PageRank (use the default parameters for `networkx.pagerank`).
2. Identifies a specific knowledge graph pattern: the "feed-forward loop" or triangle citation. This occurs when paper A cites paper B, paper B cites paper C, and paper A also cites paper C (A -> B, B -> C, A -> C).
3. Filters these triangles so that we only consider triangles where **all three** papers (A, B, and C) were published in or after a specific year. You must use a **parameterized SQL query** to perform this pattern matching and filtering directly in the database. Use `2010` as the parameter for the year threshold.
4. For each valid triangle, calculate its "importance score" by summing the PageRank values of A, B, and C.
5. Identify the top 3 triangles with the highest importance scores.
6. Save the results to `/home/user/top_triplets.json` in the exact following JSON format:

```json
[
  {
    "A": <id of paper A>,
    "B": <id of paper B>,
    "C": <id of paper C>,
    "score": <importance score>
  },
  ...
]
```
The list should be sorted in descending order of the `score`. If there is a tie, sort by A's id, then B's id, then C's id in ascending order.

Please write and run the Python script to generate this file. You may need to install `networkx` if it is not already installed.