You are a compliance officer investigating a suspected money laundering network. You have been provided with an SQLite database file located at `/home/user/financial_audit.db`. 

The database contains financial transaction records, but the system that generated it suffered a storage glitch. The index on the transaction table is corrupted and returns stale or missing rows, which has caused standard compliance tools to fail or miss critical links.

Your task is to:
1. Reverse engineer the schema of `/home/user/financial_audit.db` to understand how entities and transactions are linked.
2. Repair the corrupted database indexes so that queries return accurate data.
3. Write a Python script to perform a graph traversal that finds the shortest path of funds (fewest number of transaction hops) from the entity named `Nexus_Global` to the entity named `Apex_Solutions`.
4. Output the exact sequence of entity names in this shortest path, comma-separated (e.g., `Nexus_Global,Some_Shell_Corp,Apex_Solutions`), into a file named `/home/user/shortest_path.txt`.

Requirements:
* Use Python as your primary language to compute the shortest path.
* Ensure all database corruption is repaired (e.g., via SQLite commands) before querying, or you will retrieve a disconnected or incorrect graph.
* The output file must contain exactly one line with the comma-separated entity names.