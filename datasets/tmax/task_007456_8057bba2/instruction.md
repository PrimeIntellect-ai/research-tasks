You are acting as a technical assistant to a compliance officer auditing a financial system for potential money laundering networks. The auditing strategy relies on finding cyclic transaction paths (where money eventually loops back to the originator) within our graph database. 

You need to perform two tasks: generate parameterized graph queries using C, and process the simulated graph results using a NoSQL-style aggregation pipeline in a bash script.

**Part 1: Parameterized Cypher Query Generation (C)**
We have a list of high-risk entities in a CSV file located at `/home/user/suspicious.csv`. The file has the header `entity_id,risk_score`.
Write a C program at `/home/user/generate_queries.c` that reads this CSV file and generates a JSON lines file containing parameterized Cypher queries.

1. Your C program must take two command-line arguments: the input CSV path and the output JSONL path.
   Example: `./generate_queries /home/user/suspicious.csv /home/user/cypher_queries.jsonl`
2. For each entity in the CSV (ignoring the header), construct a parameterized Cypher query designed to find cyclic transfer paths of length between 1 and 4.
3. The exact Cypher statement must be: `MATCH path=(e:Entity {id: $entity_id})-[:TRANSFERRED*1..4]->(e) RETURN path`
4. The output must be written to the output file in JSON Lines format (one JSON object per line). Each object must have a `statement` key and a `parameters` object containing the `entity_id`.
   Example output line:
   `{"statement": "MATCH path=(e:Entity {id: $entity_id})-[:TRANSFERRED*1..4]->(e) RETURN path", "parameters": {"entity_id": "E101"}}`

**Part 2: NoSQL Aggregation Pipeline (Bash/jq)**
The graph database team has run similar queries and provided the raw results in a NoSQL-style JSON lines dump at `/home/user/graph_results.jsonl`. Each line represents an entity and an array of the lengths of the cycles found for them.
Example line: `{"entity_id": "E101", "cycle_lengths": [3, 4, 3]}`

Write a bash script at `/home/user/aggregate.sh` that uses `jq` to simulate a NoSQL aggregation pipeline.
1. The script should read `/home/user/graph_results.jsonl`.
2. It must calculate the `total_cycles` (the number of elements in the `cycle_lengths` array) and `max_cycle_length` (the maximum integer in the `cycle_lengths` array) for each entity. If `cycle_lengths` is empty, `total_cycles` should be 0 and `max_cycle_length` should be `null`.
3. The script must output a single, formatted JSON array of these objects to `/home/user/audit_report.json`.
   Example output format:
   ```json
   [
     {
       "entity_id": "E101",
       "total_cycles": 3,
       "max_cycle_length": 4
     }
   ]
   ```

Compile your C program, run it to produce `/home/user/cypher_queries.jsonl`, and execute your bash script to produce `/home/user/audit_report.json`.