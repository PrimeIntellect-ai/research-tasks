You are a data analyst tasked with processing a large network dataset using only Bash and standard GNU utilities (awk, sed, grep, join, sort, etc.). You need to extract a specific subgraph and export it into a format suitable for loading into a Neo4j graph database.

You have two files in `/home/user/data/`:
1. `nodes.csv` - Contains node information.
   Format: `node_id,label,name`
   Example: `U-102,Person,Alice Smith`
2. `edges.csv` - Contains directed edge information representing interactions.
   Format: `src_id,dst_id,relation,weight`
   Example: `U-102,U-994,KNOWS,1.5`

Your task:
Write a bash script at `/home/user/extract_subgraph.sh` that performs the following steps:
1. **Graph Traversal (Depth 2):** Starting from the target node ID `U-007`, find all nodes connected up to 2 hops away (both outgoing and incoming edges count for traversal). This means you need:
   - The root node `U-007`.
   - All nodes that have an edge to/from `U-007` (Hop 1).
   - All nodes that have an edge to/from any Hop 1 node (Hop 2).
2. **Edge Filtering:** Collect all edges where BOTH the `src_id` and `dst_id` are within the discovered set of nodes (root + hop 1 + hop 2).
3. **Cypher Export:** Convert the extracted nodes and edges into a Cypher script located at `/home/user/subgraph.cypher`.

**Cypher Output Format Constraints:**
The `subgraph.cypher` file must precisely follow this structure:
- First, define all nodes in ascending alphabetical order of their `node_id`.
  Format: `CREATE (:`<label>` {id: '`<node_id>`', name: '`<name>`'});`
- Next, an empty line.
- Finally, define all edges in ascending alphabetical order of `src_id`, then `dst_id`.
  Format: `MATCH (a {id: '`<src_id>`'}), (b {id: '`<dst_id>`'}) CREATE (a)-[:`<relation>` {weight: `<weight>`}]->(b);`

**Example Output:**
```cypher
CREATE (:Person {id: 'U-007', name: 'James Bond'});
CREATE (:Person {id: 'U-008', name: 'Alec Trevelyan'});
CREATE (:Location {id: 'L-101', name: 'London'});

MATCH (a {id: 'U-007'}), (b {id: 'L-101'}) CREATE (a)-[:VISITED {weight: 5.0}]->(b);
MATCH (a {id: 'U-007'}), (b {id: 'U-008'}) CREATE (a)-[:KNOWS {weight: 1.2}]->(b);
MATCH (a {id: 'U-008'}), (b {id: 'L-101'}) CREATE (a)-[:VISITED {weight: 3.1}]->(b);
```

**Requirements:**
- Do not install external graph databases or parsers like Python/Node.js to do the traversal. You must implement the logic using Bash utilities (e.g., `awk` is highly recommended for performance and joining).
- Ensure your script executes correctly when run as `bash /home/user/extract_subgraph.sh`.
- Deduplicate nodes and edges in the final output.
- Make sure to handle the CSV headers correctly (they should not be treated as graph nodes).