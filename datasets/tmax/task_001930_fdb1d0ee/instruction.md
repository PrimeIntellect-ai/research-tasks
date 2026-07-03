You are a Database Reliability Engineer (DBRE) tasked with managing our geographically distributed backups. We need to restore the `main_prod` database to the server `db-target-01`. However, to do this efficiently, we must route the backup file through our internal network via the path with the lowest latency.

The system uses a SQLite database located at `/home/user/backup_meta.db` to track servers, available backups, and network links between datacenters.

We have a legacy script located at `/home/user/get_links.sh`. It is intended to output the current network topology (source hostname, destination hostname, and latency in ms) by joining the `servers` and `network_links` tables. Unfortunately, the SQL query in the script has a bug (an implicit cross join) that causes it to output massively multiplied, incorrect routing information.

Your objectives are:
1. Identify and fix the SQL bug in `/home/user/get_links.sh`. The corrected query must output rows in the format `source_hostname|destination_hostname|latency`.
2. Determine which server currently holds the `main_prod` database backup by querying the `backup_meta.db` database. Let's call this the `source_server`.
3. Create a Bash script at `/home/user/calc_shortest_path.sh`. This script must:
    - Accept the topology data from the corrected `./get_links.sh` via standard input (e.g., `./get_links.sh | ./calc_shortest_path.sh`).
    - Parse the topology as a directed graph.
    - Implement a graph traversal/shortest path algorithm (like Dijkstra's or a thorough breadth-first search) entirely in Bash (or utilizing basic Unix utilities within the Bash script) to calculate the minimum latency path from the `source_server` to `db-target-01`.
4. Output the final optimal routing path and the total latency to `/home/user/restore_plan.txt` in exactly this format:
   `Path: <source_server> -> <hop1> -> ... -> db-target-01 | Total Latency: <total_ms>`

Example of the expected output file format:
`Path: backup-eu -> relay-xyz -> db-target-01 | Total Latency: 45`

Ensure all scripts are executable. You have `sqlite3` and standard Linux tools installed.