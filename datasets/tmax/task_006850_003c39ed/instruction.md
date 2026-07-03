You are a Database Administrator tasked with analyzing concurrent transaction behaviors to identify deadlocks and determine which transactions are central bottlenecks.

You have been provided an SQLite database at `/home/user/transactions.db` containing a table `locks` with the following schema:
`tx_id` (TEXT), `resource` (TEXT), `state` (TEXT - either 'GRANTED' or 'WAITING').

When a transaction (A) is 'WAITING' on a resource that is currently 'GRANTED' to another transaction (B), transaction A is waiting for transaction B. This forms a directed edge (A -> B) in a "wait-for" graph.

Your task is to:
1. Query the database to project and materialize this wait-for graph.
2. Write a Python script `/home/user/analyze_deadlocks.py` that reads the database, constructs a directed graph using the `networkx` library, and performs graph analytics:
   - Identify all simple cycles in the graph (representing deadlocks).
   - Calculate the in-degree centrality for all transactions in the graph (which transactions are waited on the most).
   - Find the single transaction with the highest in-degree centrality.
3. Export the results to `/home/user/deadlock_report.json` exactly matching this JSON structure:
   ```json
   {
     "deadlocks": [
       ["tx_A", "tx_B", "tx_C"],
       ...
     ],
     "in_degree_centrality": {
       "tx_A": 0.5,
       "tx_B": 0.25
       ...
     },
     "bottleneck_tx": "tx_A"
   }
   ```
   *Note: For the "deadlocks" list, each inner list should be a cycle returned by `networkx.simple_cycles()`. Sort the list of cycles lexicographically by the string representation of the cycles to ensure consistency.*
4. Write a bash script `/home/user/run_analysis.sh` that executes your Python script.

Make sure your script correctly builds the graph, calculates the required analytics, and writes the specific JSON format.