You are a data analyst at a logistics company. We use a proprietary, high-speed routing engine located at `/app/pathfinder` to compute shortest paths across our supply chain network. The network graph is stored in `/app/data/graph.csv`. 

Recently, we discovered a severe issue: the `pathfinder` engine has a corrupted internal index. When it processes queries for certain specific nodes, it silently falls back to a corrupted memory state and returns stale, inaccurate pathing data. 

Our engineers found that while the engine silently fails during normal execution, we can detect the bug by asking the engine to generate a query execution plan. If you run the engine with the `--explain` flag:
`/app/pathfinder --explain --graph /app/data/graph.csv --query <query_file.csv>`
it will print the query plan to standard output. If the query triggers the bug, the query plan output will contain the exact string: `[WARN] INDEX_STATE: CORRUPTED`. If the query is safe, it will output `[INFO] INDEX_STATE: VALID`.

**Your Objective:**
You must create a Bash script at `/home/user/sanitize.sh` that filters out dangerous queries. 

1. The script must accept a single argument: the path to a CSV file containing routing queries (format: `source_node,target_node,max_latency`).
2. The script must evaluate each query row (you may use `/app/pathfinder --explain` to test them).
3. The script must output the "safe" rows to `stdout` in the exact original CSV format, preserving the header if it exists.
4. "Evil" rows that trigger the corrupted index must be completely omitted from the output.

There is a stripped version of the binary at `/app/pathfinder`. You can experiment with it to understand its behavior. 
Create your final script at `/home/user/sanitize.sh` and ensure it is executable. Do not leave any temporary files behind in the final output stream.