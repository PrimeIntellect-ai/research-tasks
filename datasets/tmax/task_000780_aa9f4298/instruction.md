You are a Database Reliability Engineer tasked with modernizing a legacy backup system. 

Currently, our system relies on an old, compiled, proprietary backup utility located at `/app/legacy_graph_backup`. This utility is a stripped binary that reads a relational SQLite database backup and materializes it into a proprietary Graph Document format (JSON) for our disaster recovery graph database. 

The binary is incredibly slow and unmaintained. Your task is to reverse-engineer the output format of this binary and write a highly optimized Python script `/home/user/fast_backup.py` that performs the exact same cross-representation mapping (relational to graph) but much faster.

The input database `/home/user/prod_backup.sqlite` contains the following schema:
- `users (id, username, created_at)`
- `devices (id, user_id, device_type, os_version)`
- `logins (id, user_id, device_id, timestamp, ip_address)`

You must:
1. Analyze the output of `/app/legacy_graph_backup` by running it on `/home/user/prod_backup.sqlite`.
2. Understand the schema mapping (how rows are projected into nodes and edges in the graph JSON).
3. Write `/home/user/fast_backup.py` which takes two arguments: `python fast_backup.py <input_sqlite_path> <output_json_path>`.
4. Ensure your script uses parameterized queries and efficient data structures to minimize runtime.
5. Produce the exact same JSON structure as the legacy binary.

Your script will be tested against a massive hidden database. It must produce the structurally identical JSON output as the legacy tool but execute significantly faster to pass the automated verification.