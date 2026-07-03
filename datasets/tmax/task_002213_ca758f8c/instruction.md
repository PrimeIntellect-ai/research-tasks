You are a Database Reliability Engineer (DBRE) tasked with building a backup restoration planner. Your company manages hundreds of distinct application databases, and during a disaster recovery scenario, tables must be restored in a specific order to satisfy foreign key constraints (parents before children).

Your goal is to write a Python CLI tool at `/home/user/plan_restore.py` that takes the path to an SQLite metadata database as its only argument, analyzes the schema relationships, and outputs the safe table restoration order.

**System State & Requirements:**
1. **The Dependency Graph:** To calculate the restoration order, you must perform a topological sort. You must use the pre-vendored `networkx` package located at `/app/networkx-3.1/`. Note: Another engineer was modifying this vendored library to add telemetry and accidentally broke something in its DAG traversal module. You will need to find and fix their mistake in the `/app/networkx-3.1/` source code so you can import and use it successfully. Do not install `networkx` from pip; you must use the vendored version by modifying your `PYTHONPATH`.
2. **The Metadata Database:** The input to your script will be an SQLite database containing two tables:
   - `tables`: Columns `(id INTEGER PRIMARY KEY, table_name TEXT)`
   - `foreign_keys`: Columns `(id INTEGER PRIMARY KEY, child_table_id INTEGER, parent_table_id INTEGER)`
3. **The SQL Bug:** A junior engineer wrote a starter query to extract the edges (parent to child relationships), but it contains a critical bug (an implicit cross join) that returns totally incorrect, duplicated results. You must write a proper SQL query using explicit `JOIN`s to map the `table_name` of the parent to the `table_name` of the child.
4. **The Output:** Your script must print exactly one line to standard output: a comma-separated list of the table names in a valid topological order (parents before children). If there are independent tables or ties, `networkx`'s default `lexicographical_topological_sort` must be used to ensure deterministic output (sort alphabetically when there are ties).

**Testing:**
You can create your own dummy SQLite databases to test your script. During evaluation, an automated fuzzer will invoke your script with random, dynamically generated SQLite databases (varying the number of tables, names, and dependency chains) to ensure it is perfectly robust and mathematically correct under all schema configurations.

Write your complete solution to `/home/user/plan_restore.py` and ensure it is executable.