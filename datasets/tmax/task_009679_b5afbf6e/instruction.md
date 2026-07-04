You are a data engineer working on an ETL pipeline monitoring system. We have an SQLite database containing metadata about our ETL task dependencies and their execution logs, located at `/home/user/etl_metadata.db`.

Due to a recent pipeline bug, some queries on the execution logs return stale or duplicate rows (acting like a corrupted index). Your task is to bypass these anomalies, find the critical shortest path of our pipeline, and aggregate the execution times.

Specifically, you need to write a Python script (or use SQL and shell commands) to:
1. Connect to `/home/user/etl_metadata.db`.
2. Find the shortest path (minimum number of edges) in the directed graph of tasks from the source node `'Extract_API'` to the target node `'Load_DW'`. The edges are defined in the `dependencies` table (`source_task` -> `target_task`).
3. For each task in this shortest path, retrieve the execution duration (in seconds) from the `task_logs` table. To bypass the stale records, you must ONLY consider rows where `status = 'SUCCESS'`, and if there are multiple successful runs for a task, you must strictly pick the one with the highest `run_id`.
4. Calculate the duration in seconds for each valid task run (`end_time` - `start_time`).
5. Export the findings to a JSON file at `/home/user/critical_path_summary.json` with the exact following structure:

```json
{
  "path": ["TaskA", "TaskB", "TaskC"],
  "task_durations": {
    "TaskA": 10,
    "TaskB": 15,
    "TaskC": 20
  },
  "total_duration": 45
}
```

Ensure the `"path"` array lists the tasks in the exact order they are traversed. The durations should be integers.