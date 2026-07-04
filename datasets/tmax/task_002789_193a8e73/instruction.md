You are a data engineer building an ETL pipeline. You need to transform a relational dataset of network connection events into an optimized, pre-aggregated document format suitable for a graph database bulk loader.

You have been provided with a CSV file at `/home/user/network_events.csv` containing raw connection logs.
The CSV has no header. The columns are: `source_ip`, `target_ip`, `port`, `timestamp`.

Your task is to convert this relational data into a graph edge list in JSONL (JSON Lines) format at `/home/user/graph_edges.jsonl`. 

To optimize the downstream graph query execution plan (specifically to minimize page thrashing during bulk insert), the downstream system requires the edges to be pre-aggregated and sorted. 

Requirements:
1. **Cross-representation Mapping & Aggregation:** Convert the data into a JSONL graph edge list. You must group identical connections (same `source_ip`, `target_ip`, and `port`) and count them to create a `weight` property. Ignore the `timestamp` field.
2. **Output Schema:** Each line in `/home/user/graph_edges.jsonl` must be a valid JSON object strictly matching this structure:
   `{"source": "<source_ip>", "target": "<target_ip>", "properties": {"port": <port_number>, "weight": <count>}}`
   Note: `port` and `weight` must be integers, not strings.
3. **Physical Plan Optimization (Sorting):** The output lines in `graph_edges.jsonl` must be sorted lexicographically by `source_ip`, then lexicographically by `target_ip`, and finally numerically by `port` (ascending). 

Example expected line format:
`{"source": "192.168.1.1", "target": "10.0.0.5", "properties": {"port": 443, "weight": 3}}`

You may use standard Linux command-line tools (like `awk`, `jq`, `sort`, `uniq`) or write a short script in Python or any other available language to accomplish this. Save the final output exactly at `/home/user/graph_edges.jsonl`.