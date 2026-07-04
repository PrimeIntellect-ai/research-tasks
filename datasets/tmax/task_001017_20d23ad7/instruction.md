You are a Database Reliability Engineer. Our automated graph database backup system has a serious performance bottleneck. 

The current backup system uses a proprietary, legacy tool located at `/app/legacy_backup_bin` to query and extract subgraphs for incremental backups. This tool reads a raw binary edge list from `/home/user/graph_data.bin` and projects a localized graph. Unfortunately, it is extremely slow, likely because it executes an unoptimized query plan (doing full file scans for every depth traversal).

Your task is to write an optimized replacement program in C (`/home/user/fast_backup.c`) that implements the exact same logic but is significantly faster.

Here are the details you need:
1. **Raw Data Format**: `/home/user/graph_data.bin` contains a list of directed edges. Each edge is exactly 8 bytes: two 32-bit unsigned integers (Little Endian) representing `(source_node_id, target_node_id)`.
2. **Oracle Tool**: `/app/legacy_backup_bin` takes four arguments: 
   `/app/legacy_backup_bin <root_node_id> <max_depth> <page_size> <page_num>`
   It performs a Breadth-First Search (BFS) starting from `root_node_id` up to `max_depth` (where depth 0 is just the root node). It collects all unique reachable node IDs (including the root), sorts them in ascending order, and then paginates the result using `page_size` and `page_num` (0-indexed).
3. **Output Format**: The oracle outputs a strict JSON schema to standard output:
   `{"root": 10, "depth": 2, "total_reachable": 45, "page": 0, "results": [10, 15, 23, ...]}`
   Your replacement program must produce the exact same JSON format, including spacing.

You must:
- Reverse-engineer the behavior of `/app/legacy_backup_bin` by running it with various inputs.
- Write `/home/user/fast_backup.c` and compile it to `/home/user/fast_backup`.
- Ensure your program's query plan is optimized (e.g., read the file into memory once, build an adjacency list or use efficient indexing, then traverse).
- Your program will be tested against the legacy binary for correctness.
- Your program must achieve a **metric threshold speedup of at least 50x** compared to the legacy binary on a large dataset.