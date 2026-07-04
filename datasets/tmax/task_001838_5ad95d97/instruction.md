You are a database reliability engineer tasked with modernizing our backup management system. We have an old, undocumented compiled C tool (`/app/legacy_chain_builder`) that analyzes backup dependency graphs and outputs valid restoration chains. We lost the source code and need to rewrite it in Python.

The input to the tool is the path to a SQLite database file containing backup metadata.
The database schema is:
```sql
CREATE TABLE backups (
    backup_id INTEGER PRIMARY KEY,
    parent_id INTEGER,
    backup_type TEXT, -- 'FULL', 'DIFF', or 'INC'
    size_bytes INTEGER,
    timestamp DATETIME
);
```

Your goal is to write a Python script at `/home/user/chain_builder.py` that takes a single command-line argument (the path to the SQLite database) and produces BIT-EXACT identical standard output as the `/app/legacy_chain_builder` binary for any given database.

From our observations, the binary:
1. Finds all restoration chains that start with a 'FULL' backup and follow the `parent_id` links to subsequent backups.
2. Calculates the total size of each chain.
3. Seems to use recursive CTEs or complex joins to traverse the graph.
4. Outputs the chains in a specific text format, sorted by some criteria (likely total size or starting timestamp).
5. Has a known quirk where it occasionally miscalculates or duplicates certain paths if there are anomalous dependencies (suspected implicit cross join or missing distinct clause in its internal query). You MUST replicate its behavior exactly, quirks included, so our downstream parsing systems don't break.

You can inspect the binary `/app/legacy_chain_builder` (which is a stripped, packed executable) and run it against your own test SQLite databases to reverse-engineer the exact SQL logic, formatting, and sorting rules it uses. 

Requirements:
- Your script must be located at `/home/user/chain_builder.py`.
- It must run with Python 3.
- It must accept the SQLite DB path as `sys.argv[1]`.
- It must print the exact same standard output as the legacy binary.