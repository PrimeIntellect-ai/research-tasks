You are an AI assistant helping a scientific researcher organize and analyze a complex dataset.

I have an SQLite database located at `/home/user/experiments.db`. It contains a single table named `raw_records` with one column called `document` of type TEXT. This column stores NoSQL-style JSON documents representing experimental results. 

The JSON structure looks like this:
```json
{
  "experiment_id": "EXP-01",
  "metadata": {
    "group": "Control",
    "timestamp": 1672531200
  },
  "results": {
    "primary_metric": 42.5
  }
}
```

I need you to write a C program located at `/home/user/analyze.c` that connects to this database using the SQLite3 C API and executes a query to perform the following:
1. Extract the `group` (string), `timestamp` (integer), and `primary_metric` (float) from the JSON documents.
2. Use an SQL window function to calculate the `DENSE_RANK` of the `primary_metric` in descending order, partitioned by the `group`.
3. Order the final results primarily by `group` (ascending) and secondarily by `rank` (ascending), then by `timestamp` (ascending).

Your C program must execute this query and write the results to a CSV file at `/home/user/results.csv`. The CSV should not have a header row. Each line should be formatted exactly as:
`group,timestamp,primary_metric,rank`
(e.g., `Control,1672531200,42.5,1`)

Compile your C program into an executable named `/home/user/analyze` using `gcc` and run it to produce the `results.csv` file. Ensure you link against the `sqlite3` library.