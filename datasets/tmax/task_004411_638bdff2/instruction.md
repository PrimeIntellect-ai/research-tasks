You are a Database Reliability Engineer (DBRE) tasked with determining the correct restoration sequence for a set of microservices after a partial datacenter outage.

You have two sources of truth for the system's state:
1. A SQLite database containing backup status metadata: `/home/user/backups.sqlite`. 
   - Table `backups` schema: `(service_id TEXT PRIMARY KEY, status TEXT, last_backup_time TEXT)`
   - The `status` column will be either `'SUCCESS'` or `'FAILED'`.

2. A JSON file containing the service dependency graph: `/home/user/services.json`.
   - It contains a list of dictionaries. Each dictionary has a `"service_id"` (string) and a `"depends_on"` (list of strings).
   - If Service A depends on Service B, Service B MUST be restored before Service A.

Your task is to write a Python script at `/home/user/restore_plan.py` that performs the following:
1. Queries the SQLite database to identify all services with a `'FAILED'` backup status.
2. Reads the JSON file to build a dependency graph.
3. Projects a subgraph that *only* contains the failed services. (If a failed service depends on a successful service, ignore the successful dependency).
4. Computes a valid restoration order (topological sort) for the failed services.
5. If there are multiple valid services that can be restored at any given step (i.e., tie-breaking for nodes with an in-degree of 0), you MUST pick the one that comes first alphabetically.
6. Writes the final restoration sequence as a JSON array of strings to `/home/user/restore_order.json`.

Ensure your script runs successfully and creates the output file in the exact requested format.