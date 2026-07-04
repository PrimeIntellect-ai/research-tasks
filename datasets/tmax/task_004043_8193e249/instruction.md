You are a Database Reliability Engineer tasked with generating a prioritized database restoration plan after a simulated failure of the `auth_db` cluster. 

Your company's database dependency records are scattered across multiple systems and formats:
1. A relational export: `/home/user/relational_deps.csv` (Columns: `db,depends_on`)
2. A document store export: `/home/user/doc_deps.json` (List of JSON objects with keys `"db"` and `"requires"`, where `"requires"` is a list of database names the `"db"` depends on).

Your task:
1. Write a Python script `/home/user/backup_manager.py` that reads both dependency files and unifies them into a single directed graph. A directed edge should represent a dependency (e.g., if A depends on B, the path goes from A to B).
2. The script must identify all databases that depend (directly or indirectly) on `auth_db`.
3. For each affected database, compute the shortest path distance to `auth_db` (number of edges).
4. Output a log file at `/home/user/restore_plan.log`. The log must contain the affected databases (excluding `auth_db` itself) sorted by their shortest path distance to `auth_db` in **descending** order (so those furthest away are restored last). If distances are equal, sort the database names alphabetically in **ascending** order.
5. The format for each line in `/home/user/restore_plan.log` must be:
`<distance>: <db_name>`
For example:
`3: notification_db`
`1: user_db`

Run your script to ensure `/home/user/restore_plan.log` is generated correctly. Do not use external graph libraries like `networkx`; implement the graph traversal using standard library Python.