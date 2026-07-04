You are a database administrator tasked with optimizing and securing a custom Python-based graph querying system. 

We have a vendored version of the `networkx` library located at `/app/networkx-3.0`. However, a recent internal patch broke the `json_graph.node_link_data` module—it fails to correctly serialize or deserialize edge sources. 
Your first task is to identify and fix the deliberate perturbation in the vendored `networkx` package so that we can load our graph data.

Second, our system has been receiving queries from various clients, some of which are malicious or poorly optimized. We have collected a set of queries in JSON format.
You must build a security and performance classifier. Create a script `/home/user/detector.py` that takes a single file path as an argument. The script must parse the JSON query and exit with code `0` if the query is safe (clean), and exit with code `1` if the query is malicious or violates our performance constraints (evil).

A query is considered "evil" if ANY of the following are true:
1. It attempts to modify the graph data (e.g., contains an `"action": "delete"`, `"action": "update"`, or `"action": "insert"` key at the top level). Read-only queries have `"action": "read"`.
2. It attempts to query restricted node properties: `"password"`, `"ssn"`, or `"auth_token"` in its `"match_properties"` list.
3. It performs a pagination request with a `"limit"` strictly greater than 100.
4. It performs an unbounded graph traversal (i.e., `"max_depth"` is set to `"unbounded"` or is strictly greater than 5).

Otherwise, the query is "clean". 
We have provided sample queries in `/app/corpus/clean/` and `/app/corpus/evil/` for you to test your detector.

Finally, write a script `/home/user/summarize_graph.py` that uses the fixed `networkx` package to load the graph data from `/app/data/graph.json` (using `node_link_graph`), calculates the degree of every node, and outputs the top 5 nodes with the highest degree in JSON format to `/home/user/top_nodes.json`. The output should be a list of dictionaries, e.g., `[{"id": "node_1", "degree": 42}, ...]`, sorted in descending order of degree, and then alphabetically by node ID if there is a tie.

Ensure your scripts are completely self-contained and run in the provided Python 3 environment.