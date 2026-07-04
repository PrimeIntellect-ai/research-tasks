You are a Database Reliability Engineer (DBRE) tasked with optimizing our geo-distributed backup mesh. We have lost the original plaintext topology logs from our last major infrastructure migration, but we managed to recover a screen recording of the terminal that dumped the backup mesh connection data.

Your task has two phases:

**Phase 1: Topology Extraction**
We have a screen recording at `/app/db_logs.mp4`. The video shows a sequence of log lines detailing the backup cluster's network topology. Each line of the log describes a bidirectional network link between two database nodes and its bandwidth capacity, formatted exactly as:
`LINK NODE_A NODE_B CAPACITY`
1. Use tools like `ffmpeg` and `tesseract-ocr` (which are available or can be installed via `apt-get`) to extract the frames and read the text from this video.
2. Reconstruct the complete topology and save it to `/home/user/base_graph.txt`. The format of this file should be identical to the log lines (one `LINK u v weight` per line).

**Phase 2: Graph Query Implementation**
To ensure our backups can route around failures, we need a custom query engine that calculates the "Widest Path" (Maximum Bottleneck Path) between any two nodes.
Write a C++ program at `/home/user/backup_router.cpp` and compile it to `/home/user/backup_router` (ensure it is executable).

The program must behave as follows:
1. Read from standard input (`stdin`).
2. The first line contains two integers: $N$ (number of nodes, 0-indexed) and $E$ (number of edges).
3. The next $E$ lines contain the graph edges in the format `u v weight` (integers). The graph is undirected.
4. The next line contains an integer $Q$, the number of routing queries.
5. The next $Q$ lines each contain a query formatted as `source target`.
6. For each query, print a single integer on a new line to `stdout`: the maximum bottleneck capacity of a path between `source` and `target`. The bottleneck of a path is the minimum edge weight along that path. If no path exists between the two nodes, output `-1`.

Ensure your C++ code is highly efficient and strictly adheres to the input/output format, as it will be exhaustively tested against an automated oracle with random topologies and queries to ensure bit-exact output equivalence.