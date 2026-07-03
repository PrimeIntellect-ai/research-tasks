You are assisting a compliance officer auditing system access logs. A local MongoDB instance is running on default port 27017. It contains a database named `compliance` with a collection `access_logs`. 

The documents in `access_logs` have the following structure:
`{"event_id": "<uuid>", "timestamp": "<iso_date>", "action": "GRANT", "actor": "<username>", "target": "<username>", "resource": "<resource_name>"}`

Your task is to trace indirect access grants to a sensitive resource to identify if temporary contractors have inadvertently started a chain of access grants.

Write a Python script at `/home/user/audit.py` that fulfills these requirements:
1. It must accept two command-line arguments: `--resource` and `--source-user` using `argparse`.
2. It must connect to the local MongoDB `compliance` database.
3. It must execute a NoSQL aggregation pipeline to retrieve and filter all `"GRANT"` actions for the specified `--resource`. You must project only the `actor` and `target` fields to minimize memory usage.
4. Using the queried data, materialize a directed graph in memory (you may use the `networkx` library) where edges represent an `actor` granting access to a `target`.
5. Query this graph to find all unique users (targets) who eventually received access through a chain originating from the `--source-user`.
6. Sort the resulting list of compromised usernames alphabetically.
7. Save this exact sorted list as a JSON array of strings to `/home/user/audit_results.json`.

After writing the script, execute it to audit the `vault_prod` resource originating from `contractor_01`:
`python3 /home/user/audit.py --resource vault_prod --source-user contractor_01`