You are acting as a technical assistant for a compliance officer who is auditing an enterprise system for Segregation of Duties (SoD) violations. 

The audit logs have been exported as a directed edge list in CSV format at `/home/user/audit_logs.csv`. Each line contains a `source,target` pair representing an access event or a communication path (e.g., a User accessing a System, or a System calling another System).

We define an SoD violation as a specific knowledge graph pattern:
A "Triangle of Trust Bypassing" where:
1. Entity A connects to Entity B (A -> B)
2. Entity B connects to Entity C (B -> C)
3. Entity A connects directly to Entity C (A -> C)

Your task is to write a C++ program that:
1. Reads `/home/user/audit_logs.csv` and materializes it into a directed graph in memory.
2. Performs pattern matching to find all instances of the SoD violation motif (A -> B -> C and A -> C). 
3. Counts the number of violations originating from each source node 'A'.
4. Identifies the "Highest Risk Entity" (the node 'A' that is the source of the maximum number of these violations). If there is a tie, pick the one that comes first alphabetically.
5. Computes the out-degree centrality (total number of outgoing edges in the entire graph) of this Highest Risk Entity.

Write your C++ code to `/home/user/audit_analyzer.cpp`, compile it, and run it. 

Your program must generate a final report file at `/home/user/compliance_report.txt` with exactly the following format:
```
Highest Risk Entity: [EntityName]
Violation Count: [Number of violations]
Total Out-Degree: [Total outgoing edges of this entity]
```

Ensure the file paths are absolute and the output format matches exactly.