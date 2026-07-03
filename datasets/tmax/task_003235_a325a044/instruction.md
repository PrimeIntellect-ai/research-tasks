You are acting as a technical assistant for a compliance officer who is auditing our enterprise systems for GDPR data flow violations. 

We have a custom internal tool called `data-flow-tracer` that maps relationships across our relational databases, document stores, and a central knowledge graph. The source code for this tool is vendored at `/app/data-flow-tracer`. 

Recently, the tool has been failing to correctly map cross-representation relationships. Specifically, when generating the graph traversal paths from a User ID to external API endpoints, it seems to be dropping edges that connect document store nodes to graph nodes, leading to incomplete audits.

Your tasks are:
1. Investigate the Python source code in `/app/data-flow-tracer` and identify the perturbation or bug in the schema analysis and graph query mapping (hint: look at how the Cypher/SPARQL queries are constructed or how cross-system edges are yielded in `tracer/mapper.py`).
2. Fix the bug so that the cross-representation mapping works correctly.
3. Run the audit script provided in the package: `python3 /app/data-flow-tracer/run_audit.py --input /home/user/system_schema.json --output /home/user/audit_results.json`.

The final output must be written to `/home/user/audit_results.json`. The automated compliance verifier will grade your output against a golden reference dataset. You must achieve an accuracy score (F1-score of correctly identified violation paths) of at least 0.95.