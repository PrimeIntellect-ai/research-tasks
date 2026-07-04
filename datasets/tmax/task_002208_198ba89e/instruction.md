You are a database reliability engineer managing backups for a system that stores graph data in SQLite databases. 

We have a proprietary indexer binary located at `/app/graph_indexer` (it is a stripped, UPX-packed executable). This tool is typically used to build and update the `index_stats` table in our databases, which caches graph analytics (like node degree and clustering information) based on the `nodes` and `edges` tables.

Recently, a bug in our pipeline caused several backup databases to become silently corrupted. Specifically, the `index_stats` table contains stale rows (e.g., pointing to deleted nodes, or having incorrect degree counts). 

Your task is to create a Bash script at `/home/user/detector.sh` that takes a single argument: the path to an SQLite database file.
The script must analyze the database and output exactly `CLEAN` to standard output (with exit code 0) if the `index_stats` table perfectly matches the actual graph topology, or `CORRUPTED` (with exit code 1) if there are any discrepancies (stale rows, missing rows, or incorrect metrics).

You may use standard Linux coreutils, bash built-ins, and the `sqlite3` CLI. You can also utilize the `/app/graph_indexer` binary as a black-box oracle if it helps you determine the correct state, but be careful as it modifies the database in-place!

We have provided two directories containing sample databases for you to test against:
- `/app/corpus/clean/` contains valid databases.
- `/app/corpus/evil/` contains corrupted databases.

Your solution must correctly classify 100% of both corpora.

Ensure your script is executable (`chmod +x /home/user/detector.sh`).