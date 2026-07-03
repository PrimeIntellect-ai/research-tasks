You are acting as a technical assistant to a compliance officer auditing an organization's IT infrastructure for systemic vulnerabilities. The officer needs to identify which internal systems act as the most critical bottlenecks or central hubs for data flow, as these represent the highest risk if compromised.

You have been provided with two data sources representing different parts of the network:
1. User Access Logs (Document representation): `/home/user/access_logs.json`
   This file contains a JSON array of objects detailing which users accessed which entry-point systems. Format: `[{"user": "USERNAME", "accessed_system": "SYSTEM_NAME"}, ...]`
2. System Topology (Relational representation): `/home/user/system_topology.csv`
   This file contains a CSV detailing the downstream data flow between internal systems. Format: `source_system,target_system`

Your task is to write and execute a Python script that performs the following steps:
1. Parse both data sources and construct a single unified Directed Graph representing the entire flow of access (User -> System, and System -> System).
2. Compute the **Betweenness Centrality** for every node in this directed graph. Use the standard unweighted betweenness centrality algorithm (as implemented in `networkx.betweenness_centrality` with default parameters).
3. Filter the results to include *only* systems (do not include User nodes in your final output, though they must remain in the graph for the centrality calculation).
4. Identify the top 3 systems with the highest betweenness centrality.
5. Save the results to exactly `/home/user/audit_results.json` as a JSON array of objects, sorted in descending order of centrality.

The output JSON must strictly match this format (round the centrality score to exactly 4 decimal places):
```json
[
  {"system": "SystemName1", "centrality": 0.1234},
  {"system": "SystemName2", "centrality": 0.0567},
  {"system": "SystemName3", "centrality": 0.0123}
]
```

Please complete this task. You may install standard Python graph libraries such as `networkx` if they are not already available.