You are an AI assistant helping a bioinformatics researcher organize a complex web of datasets. The researcher has stored the metadata and dependency relationships of various datasets in an SQLite database located at `/home/user/research_data.db`.

The database contains two tables:
1. `nodes` 
   - `id` (INTEGER PRIMARY KEY)
   - `name` (TEXT)
   - `category` (TEXT)
2. `edges`
   - `source_id` (INTEGER)
   - `target_id` (INTEGER)
   *(This indicates that `source_id` depends on `target_id`)*

The researcher needs a Bash script to analyze the transitive impact of a specific dataset. 

Write a bash script at `/home/user/analyze.sh` that takes exactly one argument (the `name` of a target dataset) and performs the following operations using an SQLite query pipeline:
1. Performs a **recursive hierarchical query** (using a Recursive CTE) to find all datasets that transitively depend on the target dataset (i.e., find all paths leading *to* the target dataset).
2. Calculates the `depth` (shortest path length) from each dependent dataset to the target dataset (direct dependents have depth = 1, their dependents have depth = 2, etc.).
3. Uses a **window function** to calculate a `category_rank` for each dependent dataset. The rank should partition the datasets by their `category` and order them by `depth` (ascending). If there's a tie in depth, order alphabetically by `name` (ascending).
4. Outputs the result in CSV format with a header row, directly to `stdout`.

The output columns must be exactly:
`dependent_name,category,depth,category_rank`

Example usage:
```bash
bash /home/user/analyze.sh Dataset_C > /home/user/impact.csv
```

Constraints:
- Use `sqlite3` command-line tool within your bash script.
- Ensure the output strictly follows CSV format with headers (hint: use SQLite's `.mode csv` and `.header on`).
- Do not include the target dataset itself in the output, only datasets that depend on it.
- Your script must be executable (`chmod +x /home/user/analyze.sh` will be run by the evaluator, but make sure your code logic is complete).