I am a data engineer building an ETL pipeline to process financial transaction graphs. I am using a custom, locally vendored Python package located at `/app/graphetl-lib` to handle in-memory concurrent graph construction and querying. 

Unfortunately, we are experiencing severe issues. When I run the ETL ingestion with multiple threads, the process frequently hangs indefinitely. I suspect there is a concurrency issue—likely a deadlock occurring when two concurrent transactions attempt to add edges between the same or overlapping sets of nodes simultaneously.

Your task is twofold:

1. **Fix the Deadlock:** Inspect the vendored package at `/app/graphetl-lib`. Identify and fix the deadlock perturbation in the graph mutation logic (specifically around how locks are acquired when inserting edges). The fix must allow highly concurrent edge insertions without deadlocking, and without resorting to a single global lock (which would destroy our throughput).

2. **Query the Graph:** Once the library is fixed, write a Python script at `/home/user/analyze_graph.py`. This script must:
   - Import the fixed `graphetl` library.
   - Load the transaction data from `/app/data/transactions.csv`.
   - Use the library's graph traversal primitives (or write your own chained traversal logic using the library's API) to compute the shortest path (by number of hops) from node `CUST_739` to `CUST_882`.
   - Write the resulting path as a comma-separated string to `/home/user/shortest_path.txt`.

Our CI pipeline will verify your solution by running a throughput benchmark on your fixed library. Your fixed implementation must achieve a concurrent insertion throughput of at least 15,000 edges/second, meaning a global lock is not an acceptable solution.

System setup context:
- Python 3.10 is available.
- The vendored package is already present in the environment.
- The dataset `/app/data/transactions.csv` has two columns: `source` and `target`.