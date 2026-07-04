I am a researcher organizing a massive library of derived datasets. We track how datasets are created from one another using a SQLite database located at `/home/user/data_lineage.db`. 

We have a legacy compiled tool located at `/app/legacy_lineage` that correctly calculates the full upstream lineage of any dataset (i.e., all ancestral datasets that contributed to it). However, it's a black box, it's compiled for an old architecture, and it's too slow. 

I tried to write a Python replacement that queries the database, but my SQL query accidentally introduced an implicit cross join when trying to join the `datasets` and `transformations` tables recursively, causing it to return millions of duplicate/wrong rows and eventually crash.

I need you to write a Python script at `/home/user/fast_lineage.py` that acts as a drop-in replacement for the legacy binary. 

Requirements:
1. Your script must accept two positional arguments: the database path and the target dataset ID.
   Usage: `python3 /home/user/fast_lineage.py <db_path> <dataset_id>`
2. It must query the SQLite database using Python's built-in `sqlite3` module. You should use a parameterized Recursive Common Table Expression (CTE) to efficiently traverse the graph upstream (from the target dataset backwards through its sources).
3. The output format must be strictly identical to the legacy binary. You should experiment with `/app/legacy_lineage /home/user/data_lineage.db <some_id>` to observe how it formats its output (it prints a specific JSON structure to stdout).
4. Do not use any external graph processing libraries; rely purely on SQL (specifically recursive CTEs) to do the heavy lifting in the database engine, avoiding the cross join issue I ran into.

Please analyze the database schema, deduce the correct graph traversal rules from the legacy binary's output, and implement the fast Python equivalent.