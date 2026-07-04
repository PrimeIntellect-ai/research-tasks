You are an ETL data engineer troubleshooting a hierarchical data processing pipeline.

We have a local SQLite database at `/app/etl_data.db` containing a table with parent-child relationships, but the data model is undocumented. You will need to reverse-engineer the schema. Additionally, a previous failed migration left the index on the parent reference column corrupted, which currently causes queries to return stale or duplicate rows. 

There is also an image file at `/app/run_label.png` that contains a specific batch code printed on it.

Your task is to write a robust Bash script at `/home/user/process_node.sh` that takes a single integer argument (`NODE_ID`) and outputs a specific aggregated summary of that node's entire subtree.

The script must perform the following:
1. Extract the text batch code from `/app/run_label.png` (using `tesseract` or similar). Remove any trailing whitespaces or newlines.
2. Fix the corrupted index in the SQLite database before querying to ensure accurate results.
3. Write and execute a recursive SQL query (using CTEs) starting from the provided `NODE_ID` to find all of its descendants.
4. Calculate two metrics for the subtree (including the root `NODE_ID` itself):
   - The total sum of the `metric_value` column.
   - The maximum depth of the subtree relative to the queried node (the queried node is depth 0, its immediate children are depth 1, etc.).
5. Output exactly one line to standard output in the following format:
   `[BATCH_CODE] Node NODE_ID -> Total: SUM_VALUE, MaxDepth: DEPTH`

Example output:
`[BATCH-99X] Node 42 -> Total: 4500, MaxDepth: 3`

Ensure your script is efficient and outputs absolutely nothing else to stdout. We will automatically test your script against hundreds of different random `NODE_ID` values.