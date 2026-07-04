You are a database administrator troubleshooting a reporting pipeline. A junior developer ran a poorly constructed SQL query with an implicit cross join, resulting in a bloated CSV export full of duplicate rows. The file is located at `/home/user/query_results.csv`. 

The CSV has the following headerless format:
`Query_ID,Execution_Time_ms,Target_Table,Rows_Scanned`

Your task is to fix the result set and convert it into a paginated JSON document for the reporting dashboard. Perform the following steps:

1. Process the `/home/user/query_results.csv` file to remove all completely duplicate rows (the cross-join artifacts).
2. Sort the unique rows by `Execution_Time_ms` in strictly **descending** order. (If execution times are identical, maintain their relative original order, though all times in this file are unique).
3. Extract a specific "page" of results: we only want **offset 3, limit 4** (i.e., skip the first 3 highest execution times, and take the next 4).
4. Write a C program at `/home/user/csv_to_json.c` that reads this processed, 4-line subset from standard input (stdin) and converts it into a JSON array of documents.
5. Compile your C program to `/home/user/csv_to_json` and run your pipeline, redirecting the final JSON output to `/home/user/page.json`.

The JSON output written to `/home/user/page.json` MUST perfectly match this exact structure and whitespace (no extra spaces, no trailing newlines inside the array items, valid JSON):
```json
[
  {"query": {"id": "Q_XXX"}, "performance": {"time_ms": YYY, "scanned": ZZZ}, "table": "TABLE_NAME"},
  ...
]
```

Ensure your pipeline uses a combination of standard shell utilities and your C program to produce the final `page.json` file.