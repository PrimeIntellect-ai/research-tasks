You are acting as a compliance officer auditing a distributed database system for deadlocks and circular dependencies that violate system protocols. 

You have been provided with a raw snapshot of system resource locks in a JSON Lines file located at `/home/user/system_locks.jsonl`. This file was aggregated from multiple different database nodes, so the schema of the JSON objects is inconsistent. You will need to reverse-engineer the various data models present in the file to extract the necessary information.

Your objective is to:
1. Parse the NoSQL-style JSONL dump and build a data processing pipeline in Python to normalize the records. Extract the Process ID, the list of Resources currently held by the process, and the list of Resources requested (waiting for) by the process.
2. Construct a directed "Wait-For" graph. A directed edge exists from Process A to Process B if Process A is requesting a resource that Process B currently holds.
3. Perform a graph traversal to detect deadlocks (cycles). Specifically, find the shortest deadlock cycle that involves the flagged compliance process named `P_COMPLIANCE_AUDIT`.
4. Output the exact sequence of Process IDs in this shortest cycle to a file named `/home/user/deadlock_report.txt`. The output must be a single line of comma-separated Process IDs, starting and ending with `P_COMPLIANCE_AUDIT` (e.g., `P_COMPLIANCE_AUDIT,P99,P42,P_COMPLIANCE_AUDIT`). If there are multiple shortest cycles of the same length involving this node, output the one that is lexicographically first when represented as a string list.

Ensure your Python script handles the schema inconsistencies gracefully. You are expected to inspect the file, figure out the variations in how the node data is represented, map them correctly, and perform the shortest-path graph traversal.