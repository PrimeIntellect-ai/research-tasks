You are assisting a compliance officer who is auditing corporate access control systems. We are migrating to a new automated compliance pipeline, but the actual rules for what constitutes an "illegal access path" are locked inside a legacy, stripped, undocumented binary located at `/app/compliance_oracle`. 

This binary takes a single command-line argument: a comma-separated string representing an access path (e.g., `User_Alice,Role_Admin,Server_DB,Data_PII`) and exits with `0` if the path is compliant (legal), and `1` if the path is non-compliant (illegal/evil).

Your task is to write a Python classifier at `/home/user/evaluate_graph.py` that can evaluate entire system architectures at once. 

The system architectures are stored as JSON files representing directed graphs of access permissions. Each JSON file has the following format:
```json
{
  "nodes": [
    {"id": "n1", "type": "User", "label": "Contractor_Bob"},
    {"id": "n2", "type": "Role", "label": "External_Vendor"},
    {"id": "n3", "type": "Resource", "label": "Financial_Records"}
  ],
  "edges": [
    {"source": "n1", "target": "n2"},
    {"source": "n2", "target": "n3"}
  ]
}
```

Your script `/home/user/evaluate_graph.py` must:
1. Accept a single file path as a command-line argument.
2. Parse the JSON graph.
3. Perform a recursive traversal (graph projection) to find ALL possible hierarchical access paths originating from any node of type `User` and terminating at any node of type `Resource`. 
4. Translate each path into a comma-separated string of the node `label`s (in order from User to Resource).
5. Evaluate whether the graph contains ANY illegal paths. You may use `/app/compliance_oracle` as a black-box to test paths, or you may reverse-engineer its logic to write a highly optimized cross-query aggregation in your Python script.
6. If the graph contains 1 or more illegal paths, your script MUST print "NON-COMPLIANT" and exit with code `1`.
7. If the graph contains 0 illegal paths, your script MUST print "COMPLIANT" and exit with code `0`.

Ensure your script is robust and executable via `python3 /home/user/evaluate_graph.py <path_to_json>`. It will be tested against a hidden corpus of clean and evil graphs.