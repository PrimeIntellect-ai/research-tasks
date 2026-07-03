You are an AI assistant helping a compliance officer audit a company's cloud architecture. 

A recent export of the company's cloud architecture and Identity Access Management (IAM) has been provided to you as an SQLite database at `/home/user/architecture.db`. 

The database represents a knowledge graph with the following schema:
- `entities (id TEXT PRIMARY KEY, type TEXT, is_pii INTEGER, region TEXT)`
- `relations (source TEXT, relation TEXT, target TEXT)`

Your task is to identify compliance violations where an external user has a transitive path to read Personally Identifiable Information (PII). 

Perform the following steps:
1. Write a Python script `/home/user/audit.py` that connects to `/home/user/architecture.db`.
2. Within the script, write a single SQL query using a **Recursive CTE** to find all entities with `is_pii = 1` that are reachable from any entity of `type = 'ExternalUser'`. A path is valid if it consists of a sequence of relations where the `relation` is one of: `'ASSUMES'`, `'CALLS'`, or `'READS'`. Directionality matters (source -> target).
3. Output the `id` of every vulnerable PII entity found to `/home/user/vulnerabilities.txt`, with one ID per line, sorted alphabetically.
4. The provided database lacks indexes, making recursive queries extremely slow on large datasets. Before running your final query, execute SQL commands within your Python script to create optimal indexes on the `relations` and `entities` tables.
5. Extract the execution plan for your recursive query using `EXPLAIN QUERY PLAN`. Save the exact output of this plan interpretation to `/home/user/query_plan.txt`. Ensure your plan demonstrates the use of the indexes you created (i.e., avoids full table scans during the recursive steps).

Please write and run the necessary Python code to accomplish this. Do not modify the data in the tables, only add indexes.