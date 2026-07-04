You are an AI assistant acting on behalf of a compliance officer auditing a financial system for money laundering. We need to trace the flow of funds between two suspicious accounts.

You are given a SQLite database at `/home/user/financial_logs.db`. It contains a single table:
`transfers(id INTEGER PRIMARY KEY, sender TEXT, receiver TEXT, amount REAL, date TEXT)`

Your task is to analyze the data and generate a standardized JSON audit report. 

Perform the following:
1. **Index Strategy**: The database currently lacks indexes. Create appropriate index(es) on the `transfers` table to optimize querying by `sender` and `receiver`.
2. **Graph Traversal & Filtering**: Find all directed transaction paths from account `C-100` to account `C-999` that have a maximum of 4 hops (i.e., up to 4 transfers / 3 intermediate accounts).
   - *Filter*: Only consider paths where **every** transfer in the sequence has an `amount >= 50.0`. If any transfer in a path is below 50.0, discard the entire path.
3. **Sorting & Pagination**: For each valid path, calculate the `total_amount` (the sum of the `amount` of all transfers in that specific path).
   - Sort the discovered paths in **descending** order of their `total_amount`.
   - Keep only the **top 5** paths (pagination/limiting).
4. **Schema Validation & Output**: Save the results to `/home/user/audit_report.json`. The output must strictly validate against the following JSON schema:

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "properties": {
    "paths": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "route": {
            "type": "array",
            "items": { "type": "string" },
            "description": "The sequence of accounts, e.g. ['C-100', 'A', 'B', 'C-999']"
          },
          "total_amount": {
            "type": "number",
            "description": "The sum of all transfer amounts in this route"
          }
        },
        "required": ["route", "total_amount"]
      }
    }
  },
  "required": ["paths"]
}
```

Write any necessary scripts to accomplish this. You may use any programming language available in a standard Linux environment (e.g., Python, Node, Bash with SQLite CLI). Ensure `/home/user/audit_report.json` is created at the end.