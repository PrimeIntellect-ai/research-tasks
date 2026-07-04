You are a data engineer building ETL pipelines. Your team does not have a dedicated analytical database yet, so you need to process pipeline execution logs directly using Go. 

You have been provided with a CSV file at `/home/user/pipeline_logs.csv` containing raw execution metrics for various tasks in different ETL pipelines.

The CSV has the following headers:
`TaskID,PipelineID,TaskName,DurationSec,RowsProcessed`

Your task is to write a Go program (`/home/user/process_logs.go`) that performs data processing equivalent to SQL window functions, filtering, and aggregation. 

The Go program must execute the following logic:
1. Parse the `/home/user/pipeline_logs.csv` file.
2. Filter out any tasks where `RowsProcessed` is exactly `0`.
3. Group the tasks by `PipelineID`.
4. Within each `PipelineID` group, rank the tasks based on `DurationSec` in descending order (Rank 1 is the longest duration). If there is a tie in duration, resolve it by sorting `TaskID` in ascending alphabetical order.
5. Filter the grouped results to only keep the top 2 tasks (Rank 1 and Rank 2) for each pipeline (similar to pagination/limit).
6. For each pipeline, calculate the sum of `RowsProcessed` exclusively for these top 2 tasks.
7. Output the final processed data to `/home/user/etl_summary.json`.

The output file `/home/user/etl_summary.json` must be a pretty-printed JSON array (using 2 spaces for indentation) of objects, sorted by `PipelineID` in ascending alphabetical order. Each object must strictly match the following structure:

```json
[
  {
    "pipeline_id": "PipeA",
    "top_tasks": [
      {
        "task_id": "T5",
        "rank": 1,
        "duration_sec": 150
      },
      {
        "task_id": "T2",
        "rank": 2,
        "duration_sec": 120
      }
    ],
    "top_2_rows_processed": 1050
  }
]
```

Write the Go program, compile or run it, and ensure `/home/user/etl_summary.json` is generated correctly. Do not use any external Go libraries (only standard library packages like `encoding/csv`, `encoding/json`, `os`, `sort`, `strconv`, etc.).