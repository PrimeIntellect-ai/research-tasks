You are acting as an AI assistant for a Compliance Officer who needs to audit system accesses across a heterogeneous data environment. 

We have data stored in three different formats:
1. **User Database (Document)**: `/home/user/users.json` contains a JSON array of user objects with `id`, `name`, `dept`, and `clearance`.
2. **Access Logs (Relational/CSV)**: `/home/user/access_logs.csv` contains logs with columns `timestamp,user_id,system_id`.
3. **Org Chart (Graph/Adjacency List)**: `/home/user/org_chart.txt` represents reporting structures as space-separated pairs of `manager_id employee_id`.
4. **System Requirements (Document)**: `/home/user/systems.json` contains security requirements per system, keyed by `system_id`, with `req_dept` and `req_clearance`.

Your task is to write a parameterized Bash script at `/home/user/audit.sh` that takes exactly one argument: a `system_id`. 

The script must perform the following compliance checks to find illegal accesses to the specified `system_id`:
An access attempt is considered a **violation** if ANY of the following are true:
1. The user's `clearance` is LESS THAN the system's `req_clearance`.
2. The user's `dept` DOES NOT MATCH the system's `req_dept`, AND the user's direct manager's `dept` ALSO DOES NOT MATCH the system's `req_dept`. (If the user has no manager in the org chart, their manager's department is considered null).

The script must:
1. Cross-reference the CSV access logs for the given `system_id` against the JSON and Graph data.
2. Filter out compliant accesses, keeping only the violations.
3. Sort the violations by `timestamp` strictly in descending order.
4. Paginate/limit the output to only the top 3 most recent violations.
5. Export the final result to `/home/user/audit_results.json` in the following strict JSON array format:
```json
[
  {
    "timestamp": 1620000030,
    "user_id": "u3",
    "user_name": "Charlie",
    "violation_reason": "Clearance too low" // Use "Clearance too low" if clearance failed, "Department mismatch" if dept failed. If both failed, use "Clearance and Department failed".
  }
]
```

Run your script for `sysB` using `./audit.sh sysB` before finishing. Ensure the script is executable and the output file is perfectly formatted JSON. You may use standard Linux utilities like `jq`, `awk`, `grep`, `join`, `sort`, `head`, etc.