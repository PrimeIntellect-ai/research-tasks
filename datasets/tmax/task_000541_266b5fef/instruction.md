You are assisting a compliance officer in auditing an old identity and access management system. The system relies on a legacy, proprietary compliance engine to evaluate whether access requests are permitted based on the network graph.

We are migrating to a modern, Python-based compliance filter, but the documentation for the old system is lost.

You have access to the following resources:
1. **The Graph Database:** An undocumented SQLite database located at `/home/user/system_graph.db`. It contains the nodes (services) and edges (connections) of our network, along with metadata. You will need to reverse-engineer its schema to understand how nodes are connected.
2. **The Legacy Engine:** A stripped, compiled binary located at `/app/path_verifier`. This is our "oracle". It takes two integer arguments representing a `source_node_id` and a `target_node_id` (e.g., `/app/path_verifier 12 45`). It exits with code `0` if the access path is compliant, and code `1` if it is a compliance violation (non-compliant).

Your objective is to write a Python script `/home/user/audit_filter.py` that fully replaces the legacy engine. 

**Requirements for `/home/user/audit_filter.py`:**
1. It must accept a single command-line argument: the absolute path to a JSON file representing an access log. 
   Example format of the JSON file: `{"request_id": "req-99", "source": 15, "destination": 42, "timestamp": "2023-10-12T10:00:00Z"}`
2. It must query `/home/user/system_graph.db` to reconstruct the network and perform cross-query aggregation and graph traversal (shortest path) to evaluate the request.
3. It must determine the compliance of the request using the exact same underlying algorithmic logic as `/app/path_verifier`. You should experiment with the database and the binary oracle to deduce what constitutes a compliant path vs. a non-compliant path.
4. The script must output exactly the word `ACCEPT` to standard output if the request is compliant (equivalent to binary exit code 0).
5. The script must output exactly the word `REJECT` to standard output if the request is non-compliant (equivalent to binary exit code 1).

You must ensure your script handles complex queries efficiently, as the compliance officer will run it against large batches of historical access logs. Do not modify the SQLite database.