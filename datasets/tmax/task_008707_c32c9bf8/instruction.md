You are a Database Reliability Engineer investigating a performance bottleneck in a federated backup verification system. The system runs distributed queries across multiple backup storage engines (relational databases, document stores, and graph databases). 

You have been provided with two files:
1. `/home/user/query_plan.json`: A JSON file representing the execution plan of a slow distributed query as a Directed Acyclic Graph (DAG). 
    - `nodes`: A list of execution stages. Each node has an `id`, a `source_id` indicating the storage engine queried, and `time_ms` indicating the execution time of that stage in milliseconds.
    - `edges`: A list of data flows between stages, where `from` indicates the child stage and `to` indicates the parent stage. The root of the query plan is the node with no outgoing edges (no `from` where it is the `to`... wait, no `from` where it is the source. It only appears as `to`).

2. `/home/user/sources.csv`: A CSV file mapping `source_id` to the underlying storage `type` (e.g., `relational`, `document`, `graph`).

Your task is to write a Python script at `/home/user/analyze_plan.py` that computes the "critical path" of the query plan. The critical path is defined as the path from any leaf node (a node with no incoming data/edges) to the root node that yields the maximum total sum of `time_ms`.

Once you have identified the nodes on the critical path, map each node's `source_id` to its corresponding storage `type` using the CSV file.

Finally, your script must output the sequence of storage types along the critical path (starting from the leaf node and ending at the root node) as a single comma-separated string to the file `/home/user/critical_path_types.txt`.

For example, if the critical path consists of nodes querying `src_A` (leaf), then `src_B`, then `src_C` (root), and their types are `graph`, `relational`, and `document` respectively, the output file should contain exactly:
`graph,relational,document`

Ensure your script runs successfully and writes the output to the exact path specified.