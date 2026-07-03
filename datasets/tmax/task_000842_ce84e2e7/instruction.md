You are a data analyst working with a custom graph dataset exported from a legacy relational database. You need to write a C program that performs cross-representation mapping, graph projection, and NoSQL-style aggregation on this data.

The data is located in two pipe-delimited (`|`) files:
1. `/home/user/nodes.txt`: Contains node information.
   Format: `node_id|node_type|properties_json`
   Example: `1|User|{"status":"active","role":"admin"}`
2. `/home/user/edges.txt`: Contains directed edge information.
   Format: `src_id|tgt_id|rel_type|weight`
   Example: `1|3|MEMBER_OF|15`

Your objective is to write, compile, and execute a C program `/home/user/graph_processor.c` that accomplishes the following:

**1. Dependency Setup:**
Fetch the `cJSON` library (eJSON.h and cJSON.c) directly into `/home/user/` to parse the `properties_json` column. You can download it from its official GitHub repository (e.g., using `wget`). Compile it alongside your program.

**2. Graph Projection & Cross-Representation Mapping (Cypher Export):**
The program must read the nodes and edges, project a specific "active" subgraph, and materialize it as a Cypher script at `/home/user/active_subgraph.cypher`.
- **Node Filter:** Only include nodes where the JSON property `"status"` is strictly equal to `"active"`.
- **Edge Filter:** Only include edges where BOTH the source and target nodes are in the active subgraph, AND the edge `weight` is `>= 10`.
- **Cypher Format Requirement:** 
  For each active node, output a line exactly formatted as:
  `CREATE (n<node_id>:<node_type> {id: "<node_id>", status: "active"});`
  For each active edge, output a line exactly formatted as:
  `MATCH (a {id: "<src_id>"}), (b {id: "<tgt_id>"}) CREATE (a)-[:<rel_type> {weight: <weight>}]->(b);`
  Write all `CREATE` node statements first (sorted numerically by `node_id`), followed by all `MATCH ... CREATE` edge statements (sorted numerically by `src_id`, then `tgt_id`).

**3. NoSQL Aggregation:**
Compute an aggregation pipeline over the *entire original graph* (ignoring the filters used for the projection). Calculate the total sum of edge weights grouped by `rel_type`.
Output this as a single JSON object to `/home/user/edge_aggregation.json`.
Example format:
```json
{
  "MEMBER_OF": 40,
  "PARENT_OF": 50
}
```

**Constraints:**
- Write the logic entirely in C (`/home/user/graph_processor.c`).
- Compile the C program into an executable at `/home/user/graph_processor`.
- Run the executable to generate `/home/user/active_subgraph.cypher` and `/home/user/edge_aggregation.json`.
- Do not use any external tools (like Python or jq) to process the data; shell commands are only allowed to download dependencies, compile, and run the C program.