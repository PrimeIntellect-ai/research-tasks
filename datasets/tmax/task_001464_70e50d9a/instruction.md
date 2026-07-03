You are a Database Reliability Engineer (DBRE) tasked with optimizing the disaster recovery restore sequence for a massive distributed database system. 

The metadata for the latest backup is stored in a SQLite database located at `/home/user/backup_meta.db`. 
The database contains two tables:
1. `chunks` - Columns: `id` (INTEGER PRIMARY KEY), `size_mb` (INTEGER), `priority_score` (FLOAT).
2. `dependencies` - Columns: `chunk_id` (INTEGER), `depends_on_id` (INTEGER). This represents a directed acyclic graph (DAG) where a chunk can only be restored AFTER all the chunks it depends on have been restored.

We have a proprietary, closed-source simulation engine located at `/app/restore_eval` (a stripped binary). This tool simulates our storage layer's caching behavior and calculates the total "restore cost" (in seconds) of a given restore sequence. 

Your task is to write a Go program that:
1. Connects to `/home/user/backup_meta.db`.
2. Uses complex SQL joins and parameterized queries to extract the dependency graph and node weights.
3. Implements graph analytics (e.g., topological sorting combined with a heuristic based on `size_mb`, `priority_score`, and node out-degree/centrality) to determine the most optimal restore sequence.
4. Outputs the ordered list of `id`s (one per line) to `/home/user/optimal_plan.txt`.

Constraints & Verification:
- You must write your solution in Go.
- The output file `/home/user/optimal_plan.txt` must contain exactly all chunk IDs from the database, one per line.
- The sequence must be a valid topological sort (no chunk can appear before its dependencies).
- You can test your plan by running `/app/restore_eval /home/user/optimal_plan.txt`. The binary will output the total restore cost or an error if dependencies are violated.
- Your final goal is to generate a plan that achieves a restore cost of strictly less than `150000` as evaluated by `/app/restore_eval`. 

Please leave your Go source code at `/home/user/optimizer.go` and the final plan at `/home/user/optimal_plan.txt`.