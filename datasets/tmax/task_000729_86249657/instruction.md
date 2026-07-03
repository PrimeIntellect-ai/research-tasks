You are a database reliability engineer managing a complex pipeline of database backups. The backup jobs have dependencies on one another, represented as a directed graph stored in an SQLite database at `/home/user/backups.db`. 

Recently, the `job_dependencies` table suffered an index corruption issue which caused stale, inactive dependencies to be returned. 

Your task is to write a Python script at `/home/user/analyze_graph.py` that performs the following:

1. Connects to `/home/user/backups.db`.
2. Uses parameterized queries to retrieve only the *active* edges from the `job_dependencies` table (where `is_active = ?` and you pass `1` as the parameter).
3. Constructs a directed graph from these edges. The table has columns `source_job` (text) and `target_job` (text). An edge goes from `source_job` to `target_job`.
4. Calculates the **PageRank** of each node in the graph. You must use the `networkx` library with its default parameters for `pagerank()`.
5. Outputs the results to a JSON file at `/home/user/pagerank_report.json`.

The output JSON file MUST strictly adhere to the following schema and format constraints:
- The root must be an object with a single key `"pagerank_scores"`.
- The value of `"pagerank_scores"` must be a list of objects.
- Each object must have exactly two keys: `"job"` (string) and `"score"` (float, rounded to 4 decimal places).
- The list must be sorted in descending order of `"score"`. If there is a tie in score, sort alphabetically by `"job"`.

Example output format:
```json
{
  "pagerank_scores": [
    {
      "job": "db_backup_main",
      "score": 0.3456
    },
    {
      "job": "db_backup_replica",
      "score": 0.1234
    }
  ]
}
```

Run your script to generate `/home/user/pagerank_report.json`.