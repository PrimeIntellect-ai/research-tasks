You are a Database Reliability Engineer. We periodically backup our graph database into a relational format (SQLite). To ensure backup integrity, we run a validation tool that reconstructs the knowledge graph from the relational backup and verifies the presence of specific graph patterns (e.g., `User` -> `owns` -> `Service` -> `depends_on` -> `Database`).

A vendored Rust package for this validation exists at `/app/graph-backup-analyzer`. However, it has a severe performance issue. It currently takes over 40 seconds to validate a medium-sized backup, which causes our CI pipeline to time out. 

Your task:
1. Analyze the SQLite database backup located at `/var/backups/graph_data.db`. It has two tables: `nodes` (id, label, properties) and `edges` (source_id, target_id, relation_type).
2. Fix and optimize the Rust code in `/app/graph-backup-analyzer`. The current implementation has a severe data retrieval flaw (N+1 queries) when doing the cross-representation mapping from relational to graph.
3. Optimize the database querying within the Rust code. You should modify it to use efficient joins or bulk queries.
4. Ensure the optimized Rust program correctly outputs the validation result to `/home/user/validation.json`. The JSON must match the original schema (an array of matched path objects containing the node IDs).
5. Compile your fixed version in release mode.

The automated verification system will test your optimized binary. Your solution must correctly output the validation JSON and execute in **under 2.0 seconds**.