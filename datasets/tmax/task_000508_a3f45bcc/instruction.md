A compliance officer is auditing a system's transaction logs to identify a reported deadlock involving user processes. The system state is scattered across a relational database (tracking resource locks) and a JSON document (tracking process metadata).

You have access to the following data sources:
1. An SQLite database at `/home/user/transactions.db` with a table `locks`.
   Schema: `lock_id` (INTEGER PRIMARY KEY), `process_id` (INTEGER), `resource_id` (INTEGER), `status` (TEXT: either 'GRANTED' or 'WAITING').
2. A JSON file at `/home/user/processes.json` containing a list of dictionaries with process metadata. Each dictionary has `process_id` (int), `owner` (string), and `priority` (int).

Your task is to write a Python script at `/home/user/find_deadlock.py` that performs the following steps:
1. Query the SQLite database using complex joins to find pairs of processes where Process A is 'WAITING' for a `resource_id` that is 'GRANTED' to Process B. This represents a directed dependency: Process A -> Process B.
2. Read the `processes.json` file to map process metadata. Filter out any dependencies involving processes where the `owner` is 'system'. We are only auditing 'user' owned processes. Both Process A and Process B must be 'user' processes to be considered.
3. Project these dependencies into a directed graph (using basic Python structures or a library like `networkx`).
4. Traverse the graph to find a cycle (a deadlock). There is exactly one isolated cycle consisting entirely of 'user' processes.
5. Extract the `process_id`s involved in this cycle, sort them in ascending numerical order, and write them as a comma-separated list (e.g., `10,24,35`) to a file at `/home/user/deadlock_report.txt`.

Ensure your script handles everything end-to-end, from cross-representation mapping (SQLite + JSON) to graph projection and cycle detection. Run your script to generate the output file.