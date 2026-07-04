You are a Database Reliability Engineer investigating a set of graph database backups to identify critical network bottlenecks.

You have been provided with two backup files in JSON Lines (JSONL) format:
1. `/home/user/backups/nodes.jsonl`
2. `/home/user/backups/edges.jsonl`

Your task is to reverse-engineer the schema from these backups and write a Bash script `/home/user/process_graph.sh` that performs an analytical aggregation. You must use standard Linux command-line tools (like `jq`, `awk`, `grep`, `sort`, etc.)—no external scripting languages like Python or Node.js are allowed.

Here is the analytical requirement:
1. Identify all nodes of type `"Server"`. Each server belongs to a specific `"datacenter"` (a property in the node JSON).
2. Calculate the "total network bandwidth" for each Server node. This is defined as the sum of the `"weight"` property of all edges of relationship type `"NETWORK_LINK"` where the server is EITHER the `"src"` (source) OR `"dst"` (destination). Ignore edges that are not `"NETWORK_LINK"`.
3. For each `"datacenter"`, find the Server node with the highest total network bandwidth. (Assume there are no ties for the maximum).
4. Output a single JSON object to `/home/user/top_servers.json` where the keys are the datacenter names and the values are the IDs of the top Server nodes in those datacenters.

The output in `/home/user/top_servers.json` should look exactly like this (the order of keys does not matter, but it must be valid JSON):
```json
{
  "us-east": "s2",
  "eu-west": "s3"
}
```

Constraints:
- You must write `/home/user/process_graph.sh` and execute it so that `/home/user/top_servers.json` is generated.
- Ensure your script is executable (`chmod +x`).
- Do not install any additional packages; use standard pre-installed tools.