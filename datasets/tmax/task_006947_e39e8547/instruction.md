I am a researcher organizing a dataset of academic papers for social network analysis. I have a JSON Lines file containing metadata for thousands of papers, and I need to extract a co-authorship graph from it. 

Please write a Bash script at `/home/user/project_graph.sh` that processes the file `/home/user/papers.jsonl` and projects a materialized graph into `/home/user/coauthors.csv`. 

Here is the schema of the NoSQL documents in `/home/user/papers.jsonl`:
- `paper_id`: String, unique identifier.
- `year`: Integer, publication year.
- `authors`: Array of Strings, names of authors.
- `references`: Array of Strings, cited paper IDs.

Requirements for the data processing pipeline:
1. Filter the dataset to only include papers published in the year 2021 or later (`>= 2021`).
2. Analyze the `authors` array and map the relationships: create an edge for every pair of co-authors on the same valid paper.
3. Materialize the projected graph as a CSV file at `/home/user/coauthors.csv`.
4. The CSV must have exactly this header: `source,target`.
5. The graph must be undirected and deduplicated. To ensure uniqueness and correct formatting, for every pair of co-authors, the `source` must be alphabetically less than the `target`.
6. Sort the final CSV alphabetically by `source`, then `target` (excluding the header, which must remain at the top).

You must use Bash (with tools like `jq`, `awk`, `sort`, etc., or a lightweight embedded Python script) to complete this task. The final result should be the fully populated `/home/user/coauthors.csv` file.