You are acting as a systems compliance officer auditing an organization's internal access delegation. Recent security policies require an audit of how access privileges are propagating through employee delegations, specifically tracing potential risks from external vendor accounts to secure internal resources.

You have two exported datasets on your system:
1. A relational dump of personnel: `/home/user/employees.csv` (Format: `emp_id,name,department,clearance_level`)
2. A document-oriented log of access grants: `/home/user/access_logs.jsonl` (Format: JSON lines, e.g., `{"event_id": "evt-123", "grantor_id": "E001", "grantee_id": "E002"}`, meaning `E001` granted some access to `E002`. If the grantee is a resource instead of an employee, the field is `resource_id` instead of `grantee_id`, e.g., `{"event_id": "evt-124", "grantor_id": "E002", "resource_id": "R_SECURE_PAYMENTS"}`).

Your task is to write a Go application (in `/home/user/workspace/`) that processes both datasets to build an in-memory directed access graph. 

The Go application must perform the following analysis:
1. **Shortest Path Traversal:** Compute the shortest path of access delegations from the vendor account `E_VENDOR` to the highly sensitive resource `R_SECURE_PAYMENTS`. The path should be an array of IDs starting with `E_VENDOR` and ending with `R_SECURE_PAYMENTS`.
2. **Graph Analytics (Degree Centrality):** Calculate the out-degree (number of distinct access granting events) for each employee. Identify the top 3 employees who have granted the most access (to either other employees or resources). 
3. **Sorting & Filtering:** The top 3 list must be sorted in descending order of grants. In case of a tie in the number of grants, sort alphabetically by `emp_id`.

Your Go application must write the final results strictly to `/home/user/audit_report.json` in the following exact JSON format:
```json
{
  "shortest_path": ["E_VENDOR", "E...", "E...", "R_SECURE_PAYMENTS"],
  "top_grantors": [
    {"emp_id": "E...", "grants": 15},
    {"emp_id": "E...", "grants": 12},
    {"emp_id": "E...", "grants": 9}
  ]
}
```

Requirements:
- Ensure you initialize a Go module in `/home/user/workspace/` and fetch any necessary dependencies if you choose to use external graph or JSON parsing libraries.
- Standard library is sufficient, but external Go packages are allowed.
- Ensure the output JSON file has exactly the keys `shortest_path` and `top_grantors`.