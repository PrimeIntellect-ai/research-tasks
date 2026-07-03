You are a Database Administrator working on query optimization and data lineage analysis. 

We have a system architecture tracked in an SQLite database at `/home/user/lineage.db`. The database contains two tables:
1. `systems` (columns: `id` INTEGER PRIMARY KEY, `name` TEXT, `base_latency` INTEGER) - represents system components and their baseline processing times in milliseconds.
2. `connections` (columns: `src_id` INTEGER, `dst_id` INTEGER, `network_latency` INTEGER) - represents directed data flows between systems and the network latency in milliseconds.

Your task is to find the most optimal (lowest total latency) data retrieval path from the system named 'WebFrontend' to the system named 'ColdStorage'. 

The "total latency" of a path is calculated as:
(Sum of `network_latency` for all connections in the path) + (Sum of `base_latency` for all nodes in the path, **including** both the starting 'WebFrontend' node and the ending 'ColdStorage' node).

You may use Python, shell scripts, or raw SQL (e.g., Recursive CTEs) to solve this. 

Once you find the optimal path, write the sequence of system names (starting with 'WebFrontend' and ending with 'ColdStorage') to a file named `/home/user/optimal_path.txt`. The names should be comma-separated with no spaces (e.g., `WebFrontend,AuthService,Database,ColdStorage`).