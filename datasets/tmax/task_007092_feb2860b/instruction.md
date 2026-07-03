You are a data engineer building a lightweight ETL pipeline to transform raw document-oriented event logs into a Knowledge Graph structure. 

We have a raw event log file located at `/home/user/raw_events.json`. It contains a JSON array of events representing user interactions with products on an e-commerce platform.

Your task is to write a Bash script named `/home/user/etl.sh` that performs the following steps:

1. **NoSQL-style Document Aggregation**:
   Read `/home/user/raw_events.json` and use `jq` to filter and aggregate the data.
   - Filter the documents to include *only* events where the `"action"` is `"VIEWED"`.
   - Aggregate the filtered events to count how many times each user viewed each product.
   - Output the result as a new JSON array to `/home/user/aggregated_views.json`. 
   - The output JSON array must contain objects with exactly these keys: `"user"`, `"product"`, and `"weight"`. (e.g., `{"user": "u1", "product": "p1", "weight": 3}`). The array should be sorted by `"user"`, then `"product"`.

2. **Graph Query Language Translation (Cypher)**:
   The script must then read `/home/user/aggregated_views.json` and generate a Cypher script to load this data into a property graph.
   - Output the Cypher commands to `/home/user/graph_import.cypher`.
   - For each element in the aggregated JSON, generate exactly one line containing Cypher `MERGE` statements in this precise format:
     `MERGE (u:User {id: '<user>'}) MERGE (p:Product {id: '<product>'}) MERGE (u)-[:VIEWED {weight: <weight>}]->(p);`
   - Example output line:
     `MERGE (u:User {id: 'u1'}) MERGE (p:Product {id: 'p1'}) MERGE (u)-[:VIEWED {weight: 3}]->(p);`

Make sure your script `/home/user/etl.sh` is executable (`chmod +x /home/user/etl.sh`) and runs successfully without any manual intervention. Execute your script so that the output files (`aggregated_views.json` and `graph_import.cypher`) are generated and ready for verification.