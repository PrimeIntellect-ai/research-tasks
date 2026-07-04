You are acting as a data analyst troubleshooting a database concurrency issue. We have a set of CSV logs showing transaction wait-states, and we need to detect deadlocks.

We have a vendored copy of the `networkx` Python package located at `/app/networkx`. Unfortunately, a colleague accidentally introduced a bug into the `networkx/classes/digraph.py` file while trying to optimize it, breaking directed edge additions. 

Your tasks are:
1. Identify and fix the perturbation in the vendored `networkx` package at `/app/networkx`. The package must function correctly for building directed graphs and running basic pathfinding algorithms.
2. Write a Python script at `/home/user/detect.py` that analyzes a transaction wait-for graph.
3. Your script must run using the system Python 3, and must use the vendored `networkx` package (ensure `/app/networkx` is in your `sys.path`).

**Script Specification:**
- **Invocation:** `python3 /home/user/detect.py <csv_file> <target_tx_id>`
- **Input CSV Format:** The CSV has two columns `tx,waiting_for` (with a header row). Each row indicates that transaction `tx` is waiting for a lock held by transaction `waiting_for` (a directed edge from `tx` to `waiting_for`).
- **Logic:** Build a directed graph from the CSV. Find the *shortest* deadlock cycle that contains the transaction `target_tx_id`. A deadlock cycle is a directed cycle in the graph.
- **Output:** Print the cycle as a comma-separated list of transaction IDs to standard output, starting and ending with `target_tx_id` (e.g., `T1,T2,T3,T1`). 
- **Tie-breaking:** If there are multiple shortest cycles of the same length containing `target_tx_id`, return the one whose node sequence (excluding the final duplicate `target_tx_id`) is lexicographically smallest. (For example, `T1,A,B,T1` is smaller than `T1,B,A,T1`).
- **No Deadlock:** If the target transaction is not part of any cycle, print exactly `NO_DEADLOCK`.

Ensure your script handles isolated nodes and missing targets gracefully (printing `NO_DEADLOCK`). Your final script will be extensively fuzz-tested against a reference implementation with randomly generated transaction graphs.