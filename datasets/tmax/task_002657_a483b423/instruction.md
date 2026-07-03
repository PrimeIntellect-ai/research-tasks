You are a database reliability engineer tasked with ensuring the integrity of our graph database backup manifests. We use a custom proprietary Python library, `graph-backup-lib`, to parse and validate dependency graphs of our distributed backups. 

Recently, some backup agents have been generating malformed or malicious manifests (e.g., cyclic dependencies, missing root nodes, or schema violations) that corrupt our central registry.

Your task has two parts:
1. Fix the vendored package: The `graph-backup-lib` source code is located at `/app/graph-backup-lib`. It currently has a bug preventing it from initializing properly. Fix the package so it can be imported and run.
2. Create a Python script `/home/user/manifest_filter.py` that acts as a classifier/sanitizer. It must read a directory of JSON backup manifests, use `graph-backup-lib` (and standard libraries) to parse the graph structures, and output either "ACCEPT" or "REJECT" for each file based on the following criteria:
   - A valid manifest must have a single root node (a node with no incoming edges).
   - The backup graph must not contain any cycles (it must be a Directed Acyclic Graph).
   - Every node must have a `timestamp` field matching the regex `^\d{10}$` (Unix epoch).
   - Every node must have a `checksum` field.

The script must have the following CLI signature:
`python /home/user/manifest_filter.py <path_to_directory_with_json_files>`

For each `.json` file in the directory, the script must print exactly one line to standard output in the format:
`<filename>: ACCEPT` or `<filename>: REJECT`

Your script will be tested against two datasets (clean and evil manifests) to ensure it correctly classifies them.