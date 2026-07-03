You are a Database Reliability Engineer managing an enterprise backup system. The backup dependency order is currently determined by a proprietary, unmaintained, and heavily stripped binary located at `/app/backup_path_oracle`. This tool is becoming a bottleneck in our infrastructure pipeline.

Your objective is to replace this binary by writing a Python 3 script at `/home/user/backup_planner.py` that behaves **exactly** like the oracle.

We know the following about the domain logic the binary implements, but some edge cases (like tie-breaking or unreachable nodes) might need to be deduced by testing against the binary yourself:

1. **Input Representation:** Both tools take a single argument: the path to a JSON file representing the backup dependency graph.
   - `nodes`: A list of dictionaries with `id` (integer) and `size` (integer, in GB).
   - `edges`: A list of dictionaries with `source` (integer ID), `target` (integer ID), and `transfer_time` (integer, acting as edge cost).

2. **Graph Processing & Traversal:**
   - The system identifies "primary" databases. A primary database is any node with an in-degree of 0 (no dependencies).
   - For every node in the graph, it calculates the minimum `transfer_time` distance from *any* primary database (using shortest-path traversal).
   - It computes a "Backup Priority Score" for each node using the formula: `size * (1 + min_transfer_time)`.
   - Primary databases, and databases that are entirely unreachable from any primary database, are treated as having a `min_transfer_time` of 0.

3. **Output Export:**
   - The tool outputs a single line to standard output containing a comma-separated list of node IDs sorted by their Backup Priority Score in descending order.
   - You must deduce the tie-breaking rules by generating test JSON files, feeding them to `/app/backup_path_oracle`, and observing its output.

**Requirements:**
- Implement the exact algorithm in `/home/user/backup_planner.py`.
- Ensure it accepts the input JSON file path as `sys.argv[1]`.
- Output must be bit-for-bit identical to `/app/backup_path_oracle` across all edge cases (graph cycles, multiple components, tie-breakers).
- You may use standard Python libraries or `networkx` if you choose to install it.