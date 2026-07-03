As a compliance officer auditing our internal service architecture, I need to identify if there are any unauthorized direct or indirect data flows of Personally Identifiable Information (PII) from our public-facing `Web` service to our highly restricted `ProfileDB` service.

You have been provided with an export of our service communication graph in CSV format at `/home/user/system_graph.csv`. The file has the following header:
`source,target,latency,data_tags`

Your task is to:
1. Write a C++ program at `/home/user/audit.cpp` that reads `/home/user/system_graph.csv`.
2. Project and materialize a subgraph that ONLY includes edges where the `data_tags` column contains the exact substring `"PII"`. Ignore all other edges.
3. Traverse this materialized subgraph to compute the shortest path (based on the `latency` column) from the `Web` service to the `ProfileDB` service.
4. Output the result to a file named `/home/user/compliance_report.txt` in the exact format:
`Violation Path: Node1->Node2->Node3, Total Latency: X`
(where Node1 is Web, the last node is ProfileDB, and X is the sum of latencies on the path).

You must compile your C++ code to an executable named `/home/user/audit` and run it so that the output file is generated.