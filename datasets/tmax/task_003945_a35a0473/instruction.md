You are acting as an AI assistant for a network science researcher organizing a dataset of academic papers and their citations.

The researcher has two raw CSV files in their home directory:
1. `/home/user/papers.csv` - Contains metadata about papers. 
   Columns: `id,title,year`
2. `/home/user/citations.csv` - Contains directed citation edges (who cited whom). 
   Columns: `citer_id,cited_id` (meaning the paper with `citer_id` cites the paper with `cited_id`).

The researcher needs a robust, Bash-callable tool to query the shortest citation chain between two papers and export the enriched subgraph path as a JSON array. 

Your task is to write a Bash script located at `/home/user/find_path.sh` that does the following:
1. Accepts exactly two arguments: the `START_ID` (the paper making the citation) and the `END_ID` (the paper being cited at the end of the chain).
2. Uses standard command-line tools (like `sqlite3`, `awk`, `jq`, etc.) to compute the shortest directed path from `START_ID` to `END_ID` using the `citations.csv` file.
3. If multiple paths have the same shortest length, select the path that is lexicographically first when the sequence of node IDs is joined by commas (e.g., `P01,P02,P09` is preferred over `P01,P05,P09`).
4. Joins the nodes in this path with `papers.csv` to retrieve the `title` and `year`.
5. Outputs the result to `STDOUT` as a strictly formatted JSON array of objects, ordered from the start of the path to the end.

The JSON output must have exactly this structure:
```json
[
  {
    "step": 1,
    "id": "P001",
    "title": "Introduction to Graphs",
    "year": 2010
  },
  {
    "step": 2,
    "id": "P005",
    "title": "Advanced Traversals",
    "year": 2015
  }
]
```

Requirements:
- Ensure the script is executable (`chmod +x /home/user/find_path.sh`).
- Use `sqlite3`'s recursive CTEs or write an `awk`/Bash graph traversal. `sqlite3` is highly recommended for this.
- Ensure the script outputs *only* the JSON array to standard out.
- Test your script by running `/home/user/find_path.sh P001 P005` (assuming those IDs exist in the dataset you will work with).