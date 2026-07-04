You are acting as a compliance officer auditing an internal corporate network. We have an undocumented SQLite database located at `/home/user/compliance_audit.db` containing employee records, internal communications, systems, and access logs. 

Your objective is to identify the most central employees in the communication network and determine the latest highly sensitive system each of these key individuals has accessed.

Please perform the following steps:
1. **Reverse Engineer the Schema**: Inspect `/home/user/compliance_audit.db` to understand its table structure. There are tables for employees, communications (a directed graph of messages), systems, and system access logs.
2. **Graph Analytics**: Using Python and the `networkx` library, build a directed graph from the communications table. The `sender_id` should be the source, and `receiver_id` should be the target. Calculate the PageRank of each employee. Use `networkx.pagerank(G, alpha=0.85, max_iter=100)`.
3. **Window Functions & Aggregation**: Identify the Top 3 employees with the highest PageRank scores. For these 3 employees, use a SQL Window Function (e.g., `ROW_NUMBER()`) to query the database and find the *most recently accessed* system that is marked with a sensitivity level of 'High'. 
4. **Format Conversion & Export**: Export the results to a JSON file at `/home/user/audit_report.json`.

The output JSON must be an array of objects, sorted in descending order of PageRank score. If there's a tie in PageRank, sort by employee_id ascending. The JSON should have exactly this format:
```json
[
  {
    "employee_id": 1,
    "employee_name": "Alice Smith",
    "pagerank_score": 0.3512,
    "latest_high_risk_system": "Financial_Ledger"
  },
  ...
]
```
*Note: Round the `pagerank_score` to exactly 4 decimal places.*