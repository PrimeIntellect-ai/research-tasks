You are acting as a compliance officer auditing an organization's internal IT systems. You need to analyze the company's access control graph to find compliance violations.

The organization's access control and architectural data has been exported as an RDF Turtle file located at `/home/user/org_architecture.ttl`. This graph uses the namespace prefix `org: <http://example.org/ns#>`.

The graph contains:
- `org:User` entities
- `org:Role` entities (e.g., `org:Developer`, `org:Auditor`, `org:Admin`)
- `org:Resource` entities (e.g., `org:Production_DB`, `org:Test_DB`)
- Relationships:
  - `?user org:hasRole ?role`
  - `?user org:hasAccess ?access`
  - `?access org:targetResource ?resource`
  - `?access org:accessType "READ"` or `"WRITE"`

Your task is to write a Python script (`/home/user/audit_script.py`) that analyzes this graph using SPARQL queries (e.g., via the `rdflib` library) to identify two specific types of compliance violations:

1. **Separation of Duties (SoD) Violation**: A user cannot hold both the `org:Developer` and `org:Auditor` roles simultaneously.
2. **Least Privilege (LP) Violation**: A user with the `org:Developer` role must not have an access type of `"WRITE"` to the `org:Production_DB`.

Your script must:
1. Load the RDF file.
2. Run SPARQL queries to extract users who violate Rule 1 and Rule 2.
3. Chain and aggregate the results across the queries to build a profile of "High Risk" users.
4. Output a JSON report strictly formatted and saved to `/home/user/compliance_audit_report.json`.

The output JSON must match the following format exactly:
```json
{
  "total_violations": <integer representing the total count of individual violations across all users>,
  "high_risk_users": [
    {
      "user_uri": "http://example.org/ns#UserName",
      "violations": [
        "SoD_Dev_Auditor",
        "LP_Dev_Write_Prod"
      ]
    }
  ]
}
```

Constraints & Requirements:
- You may install any necessary Python packages (like `rdflib`) using standard bash tools.
- The `high_risk_users` list must be sorted alphabetically by `user_uri`.
- The `violations` list inside each user object must be sorted alphabetically.
- If a user has no violations, they should NOT appear in the `high_risk_users` list.
- Use Python 3 to write your script.