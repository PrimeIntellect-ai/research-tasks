You are a Database Reliability Engineer (DBRE) responsible for managing a large fleet of interdependent database backups. Our backup orchestration system exports metadata about each database's backup job, including its duration and upstream dependencies (which databases must be backed up before it, to ensure data consistency across cross-database ETL syncs).

Recently, the backup orchestration has been failing because of cyclical dependencies introduced by rogue schema migrations, and backup windows are taking too long.

I have placed a JSON export of the backup job metadata at `/home/user/backup_metadata.json`.

Your task is to write a Go program (`/home/user/analyze_backups.go`) that parses this metadata, reverse-engineers the implicit dependency graph, performs graph analytics, and outputs a JSON report to `/home/user/report.json`.

Here are the requirements for your Go program:

1. **Cycle Detection:** Analyze the dependency graph (where A `depends_on` B means there is a directed edge from B to A). Identify any backup jobs that are part of a cyclical dependency (Strongly Connected Components of size > 1).
2. **DAG Conversion:** Create a filtered version of the graph that entirely excludes any jobs identified in step 1 (and removes any edges connected to them). The remaining graph will be a Directed Acyclic Graph (DAG).
3. **Graph Analytics (Centrality):** On the filtered DAG, determine the "criticality" of each job by counting its *direct* out-degree (how many jobs directly depend on it). Find the top 3 jobs with the highest direct out-degree. If there is a tie, resolve it by sorting the `job_id` alphabetically (ascending).
4. **Critical Path (Cross-query aggregation):** On the filtered DAG, calculate the critical path duration. This is the maximum total `duration_minutes` of any valid path from a source node (in-degree 0) to a sink node (out-degree 0). The duration of a path is the sum of the durations of all nodes on that path.

The output at `/home/user/report.json` must exactly match this structure:
```json
{
  "cyclical_jobs": ["job_X", "job_Y", "job_Z"], 
  "top_critical_jobs": ["job_A", "job_B", "job_C"],
  "critical_path_duration": 120
}
```
*Note: `cyclical_jobs` must be a flat array of job IDs sorted alphabetically. `top_critical_jobs` must be exactly 3 job IDs sorted by out-degree descending, then alphabetically.*

You may use standard Go libraries. Compile and run your Go program to generate the report.