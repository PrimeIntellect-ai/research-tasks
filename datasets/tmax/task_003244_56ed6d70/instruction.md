You are an IT compliance officer auditing a company's internal data transfer system for potential unauthorized data exfiltration. 

You have been provided with an export of the transfer logs in JSON Lines (NoSQL document) format. The file is located at `/home/user/audit_data/transfers.jsonl`. 

Each line is a JSON object representing a data transfer between internal system nodes. The schema looks like this:
`{"tx_id": "tx_001", "source": "NODE_A", "target": "NODE_B", "bytes": 1024, "status": "COMPLETED"}`

Your objective is to analyze this dataset using any programming language or command-line tools you prefer, performing aggregation and graph analytics to uncover suspicious activity.

Perform the following tasks:
1. **Filter and Aggregate (NoSQL style pipeline):**
   - Filter out any transfers where the `status` is NOT exactly `"COMPLETED"`.
   - Group the remaining completed transfers by the `source` node.
   - Sum the total `bytes` transferred out for each source node.
   - Identify the single node that has transferred the *highest total bytes* across all completed transactions. Let's call this the `MAX_SENDER`.

2. **Graph Traversal (Shortest Path):**
   - Treat the completed transfers as a directed, unweighted graph where `source` is the origin node and `target` is the destination node.
   - Compute the shortest path (minimum number of hops) from `NODE_SUSPECT` to `NODE_VAULT`.

3. **Report Generation:**
   Create a report file strictly formatted and saved to `/home/user/audit_report.txt` containing exactly the following three lines (replace the bracketed placeholders with your computed values):

   ```
   Highest Transfer Node: [MAX_SENDER]
   Highest Transfer Bytes: [TOTAL_BYTES_FOR_MAX_SENDER]
   Shortest Path Length: [NUMBER_OF_HOPS]
   ```

   *Note: The shortest path length is the number of edges. For example, A -> B -> C is a length of 2.*