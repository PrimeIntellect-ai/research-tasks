You are a Database Reliability Engineer responsible for managing backups of a NoSQL graph database. As part of the daily backup verification process, we export the graph topology into a JSON Lines format and run an aggregation pipeline to ensure data integrity. 

Currently, our validation tool, which computes 2-hop aggregation paths from parameterized root nodes, is failing SLA requirements. It takes too long to process even a mid-sized backup. The source code for this internal tool is provided as a vendored package.

Your task is to fix and optimize the query engine within this tool and generate the final validation report.

Requirements:
1. The tool source is located at `/app/graph_backup_validator-1.0.0/`.
2. Inspect the build system (`Makefile`). There is a misconfiguration causing it to build inefficiently. Fix the build system.
3. Inspect `src/query.c`. The function `find_edges_from_node` constructs the aggregation query plan. It currently uses an unoptimized linear scan over the edge list. Fortunately, the edge list is pre-sorted by `src_id` during the data load phase. Rewrite this query plan execution to use binary search (`bsearch` or custom logic) to locate edges in O(log N) time.
4. Recompile the tool.
5. The graph backup file is located at `/home/user/graph_export.jsonl`.
6. Run the compiled executable to generate the validation report:
   `./validator --data /home/user/graph_export.jsonl --roots 15,1024,5000,9999 --depth 2 > /home/user/validation_report.csv`

The final output `/home/user/validation_report.csv` must exactly match the format:
```csv
root_id,aggregate_weight
15,<value>
1024,<value>
...
```

To succeed, your optimizations must reduce the execution time below the hard SLA threshold of 0.2 seconds (the current unoptimized build takes over 3 seconds).