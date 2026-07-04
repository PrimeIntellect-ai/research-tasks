You are tasked with resolving a query reliability issue in a read-only SQLite database located at `/home/user/data.db`. The database contains a knowledge graph consisting of `nodes` and `edges`. 

Recently, we discovered that standard hierarchical queries are returning stale or incorrect rows. A former database administrator noted that an index on the `edges` table was corrupted during a failed disk migration. Because the database file is located on a read-only mount, you cannot drop or rebuild the index. You must write a query that fundamentally bypasses this corrupted index to retrieve the correct, live data.

Your objective is to create a Bash script at `/home/user/solve.sh` that takes a single integer argument (`START_NODE_ID`). The script must:
1. Connect to `/home/user/data.db`.
2. Perform a recursive or hierarchical query to find all unique nodes reachable from `START_NODE_ID` within exactly 1 to 3 hops (inclusive). The start node itself should only be included if it is reachable via a cycle.
3. Explicitly bypass the corrupted index so that the query engine reads the true table data instead of the stale index. 
4. Output the `name`s of all these reachable nodes to `stdout`, one name per line, sorted alphabetically.

We have provided a reference implementation—a stripped binary at `/app/query_oracle`. This oracle correctly bypasses the corrupted index and implements the exact traversal logic expected. You can test your script's behavior against it by running `/app/query_oracle <START_NODE_ID>`.

Your script `/home/user/solve.sh` must precisely match the output of `/app/query_oracle` for any valid node ID. Automated verifiers will fuzz your script with numerous random node IDs and strictly compare the outputs against the oracle.