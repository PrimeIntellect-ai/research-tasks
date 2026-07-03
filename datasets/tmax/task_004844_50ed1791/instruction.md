You are a Database Reliability Engineer investigating a potential data corruption issue that might have propagated into the backup storage infrastructure.

An SQLite database at `/home/user/backups.db` stores a dependency graph of the backup architecture. It tracks databases, backup jobs, and storage volumes. 

The database contains two tables:
1. `assets`: columns `id` (INTEGER PRIMARY KEY), `name` (TEXT), `type` (TEXT), `is_corrupted` (INTEGER).
2. `links`: columns `src` (INTEGER), `dst` (INTEGER), `status` (TEXT). This represents a directed edge from `src` to `dst`.

Some links in the database are from an old schema and are marked with `status = 'stale'`. They must be ignored. You should only traverse links where `status = 'active'`.

Your task:
1. Write a Go program at `/home/user/analyze.go` to analyze this graph.
2. Find all assets with `is_corrupted = 1`.
3. Traverse the graph via directed `active` links to find all downstream assets of type `storage` that are reachable from any corrupted asset.
4. Output the `name` of these compromised storage assets to a file named `/home/user/compromised_backups.txt`, with one name per line, sorted in alphabetical order.

You may need to initialize a Go module and install an SQLite driver (e.g., `github.com/mattn/go-sqlite3`) to interact with the database. Execute your program to generate the required output file.