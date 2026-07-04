You are a Database Reliability Engineer (DBRE) dealing with a corrupted incremental backup metadata repository. 

Our backup metadata is modeled as a NoSQL document graph where each incremental backup references a parent backup. We use an in-house Python library called `graph_backup_store` to parse and query this data. The library is vendored at `/app/graph_backup_store`.

Recently, our backup lineage tracing started failing. It appears that the internal indexing mechanism of `graph_backup_store` is corrupted—it occasionally returns stale or self-referential parent IDs, causing infinite loops when we try to trace a backup to its root full backup. 

Your task:
1. Identify and fix the bug in the vendored package `/app/graph_backup_store` that is causing the corrupted index lookups.
2. Write a Python script at `/home/user/get_lineage.py` that uses the fixed `graph_backup_store` package to trace the lineage of a given backup ID.
3. The script must accept exactly one argument (a backup ID, string or integer) and print the lineage path from that backup to the root backup (which has no parent).
4. The output must strictly be the IDs joined by ` -> `. Example output: `backup_105 -> backup_72 -> backup_12 -> backup_1`.
5. The dataset is located at `/home/user/backups.json`.

Ensure your script handles the recursive graph querying efficiently using the package's API. Do not write your own JSON parser; you must use the vendored `graph_backup_store` package.

The testing environment will verify your script against hundreds of different backup IDs to ensure it behaves exactly like our reference implementation and produces the bit-exact output.