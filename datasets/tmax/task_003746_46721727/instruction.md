You are acting as a data compliance officer auditing a corporate network for anomalous access patterns and potential data exfiltration. 

We have a multi-service compliance environment running locally:
1. **PostgreSQL** (Port 5432, Database: `audit`, User: `postgres`, Password: `password`): Contains a table `network_graph` with columns `source_node` (VARCHAR), `dest_node` (VARCHAR), and `cost` (INT). This represents the corporate network topology and trust relationships.
2. **Redis** (Port 6379): Contains active session metadata (you may not need this directly, but it must remain running for the backend API).
3. **Audit API** (Flask, Port 8000): A simulated internal service.

You are tasked with building an automated compliance classifier. 
In `/app/corpus/clean/`, there are JSON files representing normal daily access logs. 
In `/app/corpus/evil/`, there are JSON files containing anomalous access patterns. 
Each JSON file contains an array of access events in this format:
```json
[
  {"timestamp": "2023-10-01T10:00:00Z", "user_id": "u123", "source": "VLAN_10", "target": "DB_CORE"},
  ...
]
```

Your objective is to create a Python script at `/home/user/classifier.py` that takes the path to a JSON log file as its first command-line argument and prints exactly `CLEAN` or `EVIL` to standard output.

A log file is considered `EVIL` if **any** of the following conditions are met for any event in the file; otherwise, it is `CLEAN`:
1. **Network Trust Violation (Graph Traversal):** An event's `source` to `target` has NO valid path in the PostgreSQL `network_graph` table, OR the shortest path (minimum total `cost`) between them strictly exceeds 15. You must use SQL (e.g., recursive CTEs) to determine this.
2. **Velocity Violation (Analytical Aggregation):** A single `user_id` makes more than 3 access attempts (i.e., 4 or more) within any 10-minute rolling window. You should insert the file's data into a temporary table and use SQL window functions to evaluate this.

**Requirements:**
- Your script must run as: `python3 /home/user/classifier.py <path_to_json>`
- Output must be exactly the string `CLEAN` or `EVIL` (followed by a newline).
- Do not print any other debugging information to standard output.
- Optimize your queries so the script executes in under 2 seconds per file. You may interpret query plans (e.g., `EXPLAIN`) to ensure your recursive CTEs and window aggregations are efficient.

The services can be started by running `/app/start_services.sh` if they are not already running.