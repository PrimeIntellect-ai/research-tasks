You are assisting a compliance officer who is auditing internal communication systems for potential information barriers breaches.

We have a raw export of communication logs located at `/home/user/audit_logs.jsonl`. Each line is a JSON object representing a single message, with the following format:
`{"msg_id": "...", "sender": "userA@corp.com", "recipient": "userB@corp.com", "timestamp": 1690000000, "has_attachment": true}`

Your task is to write a Python script at `/home/user/audit_graph.py` that processes this log file to project and materialize a directed communication graph, and then execute it to generate a specific report.

The script must do the following:
1. **Graph Projection**: Aggregate the raw events into directed edges. An edge from `sender` to `recipient` has a `weight` equal to the total number of messages sent from that sender to that recipient.
2. **Filtering**: Drop any edges where the `weight` is less than 3 (we only care about sustained communication).
3. **Sorting**: Sort the resulting edges primarily by `weight` in descending order. If weights are tied, sort alphabetically by `source` (sender) ascending, and then by `target` (recipient) ascending.
4. **Pagination**: The script must accept two command-line arguments: `--page` (1-indexed) and `--page-size`. It should extract only the slice of the sorted edges corresponding to the requested page.
5. **Output Schema Validation**: The script must output the paginated result to a file named `/home/user/projected_graph.json`. The output must be a strictly formatted JSON array of objects. Each object must have exactly these keys and value types:
   - `source` (string)
   - `target` (string)
   - `weight` (integer)

After writing the script, execute it to generate the report for **Page 2** with a **Page Size of 2** (`--page 2 --page-size 2`).

Ensure your final output file strictly matches the requested JSON schema.