You are acting as an AI assistant to a corporate compliance officer. We are auditing our internal systems for an unauthorized data exfiltration incident. 

Here is what you need to do:

1. **Identify the Audit Target:**
   You have been provided with a scanned memo at `/app/incident_memo.png`. Use standard OCR tools (like `tesseract`) to read the text. The memo contains a string in the format `AUDIT_ROOT: <NODE_ID>`. Extract this `<NODE_ID>`.

2. **Graph Pattern Matching & Aggregation:**
   We have two datasets representing our system knowledge graph:
   * `/app/network_traffic.csv`: An edge list of network connections. Columns: `src_node, dst_node, protocol, bytes_transferred`.
   * `/app/node_metadata.json`: A document store of node details. Format: `[{"node": "...", "department": "...", "owner_id": "..."}, ...]`.

   Using only Bash shell commands, coreutils, `awk`, `jq`, and/or `sqlite3`, find all "2-hop" exfiltration paths starting from the `<NODE_ID>` you extracted. Specifically, find all distinct destination nodes (`Z`) where `<NODE_ID>` connected to some intermediate node (`Y`) via the `HTTPS` protocol, and then `Y` connected to `Z` via the `SCP` protocol. 

   For each compromised final node `Z`, calculate the **total bytes transferred** from *all* `Y` -> `Z` (via `SCP`) connections. 

3. **Cross-Representation Mapping:**
   Join your aggregated results with `/app/node_metadata.json` to find the `department` for each node `Z`.

4. **Serve the Audit Report (Multi-protocol):**
   You must expose your findings via a simple HTTP API using purely Bash (e.g., using `nc` or `socat`). 
   * Write a Bash script at `/home/user/serve_report.sh` that listens continuously on `127.0.0.1:8080`.
   * When it receives an `HTTP GET /audit-report` request, it must return an `HTTP/1.1 200 OK` response with a `Content-Type: application/json` header.
   * The response body must be a JSON array of objects, sorted descending by total bytes. Format:
     `[{"target_node": "Z", "department": "DepName", "total_scp_bytes": 1500}, ...]`

Start the server in the background once it's ready. The automated verification system will test your HTTP endpoint.