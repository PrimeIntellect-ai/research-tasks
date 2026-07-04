You are a data engineer building a lightweight ETL pipeline. We have a raw NoSQL export of server communication logs in JSON Lines format located at `/home/user/server_logs.jsonl`. 

Your task is to write a bash script at `/home/user/process_graph.sh` that performs the following steps:
1. **NoSQL Aggregation & Graph Projection**: Parse the JSON Lines file and filter out any records where the `"status"` is not `"OK"`. Project the remaining records into a directed graph of `source` -> `target` connections.
2. **Graph Analytics**: Calculate the *in-degree centrality* for every target server. For this task, "in-degree" is defined as the total number of successful (`"status": "OK"`) connections made *to* that server.
3. **Output Schema Validation**: Identify the top 3 targeted servers (highest in-degree). Write the result to `/home/user/top_targets.json`. The output must be a strict JSON array of objects with exactly this schema:
   `[{"server": "<server_name>", "in_degree": <integer_count>}, ...]`
   The array must be sorted in descending order of `in_degree`. If there is a tie, sort alphabetically by server name in ascending order.

Ensure your script `/home/user/process_graph.sh` is executable and runs successfully, generating the required `/home/user/top_targets.json` file. You may use standard Unix text processing tools (`jq`, `awk`, `sort`, `uniq`, etc.) or inline Python if you prefer, but the entry point must be the bash script.