You are a Database Reliability Engineer managing backup systems. Our backup metadata is exported from a NoSQL database as a JSONL (JSON Lines) file. Each line represents a backup snapshot with a structure like:
`{"id": "snap-003", "type": "incremental", "parent": "snap-002", "timestamp": 1690000200}`

Full backups have `"type": "full"` and no `"parent"` key. Incremental backups have `"type": "incremental"` and a `"parent"` key pointing to the previous snapshot.

We use an internal tool to compute the restore chain (a graph traversal from a target snapshot back to its root full backup, returning the sequence from full to target). The source for this tool is vendored at `/app/bkp-graph-1.0.0/`.

Unfortunately, the vendored package is currently broken:
1. It fails to build/install due to a perturbation in its configuration.
2. The core logic has a bug related to the NoSQL JSON structure mapping, causing traversal to fail.

Your task:
1. Fix the vendored package in `/app/bkp-graph-1.0.0/`.
2. Run whatever build or installation steps are necessary so that the executable is available at `/home/user/bin/get_chain.sh`.
3. Ensure that running `/home/user/bin/get_chain.sh <path_to_jsonl> <target_id>` prints exactly the comma-separated restore chain (e.g., `snap-001,snap-002,snap-003`), followed by a newline, to standard output.

You must ensure your fixed script correctly handles the JSONL format and strictly performs the graph traversal to find the path from the root full backup to the requested target backup. Do not print any extraneous text.