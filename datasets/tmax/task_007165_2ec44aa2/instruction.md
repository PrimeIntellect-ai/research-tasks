You are a Database Reliability Engineer (DBRE) responsible for managing backup infrastructure. Our organization stores its physical network topology, database instances, and storage nodes in an RDF graph. 

Some of our databases have failed their recent backups and need to be routed to alternative storage nodes. You need to write a Python script `/home/user/backup_router.py` that processes this RDF graph, finds the unbacked databases, and calculates the optimal (lowest latency) network path to a storage node that has enough capacity to hold the backup.

Here are your instructions:

1. **Environment Setup**: 
   - Install any required Python libraries. You will likely need `rdflib`, `networkx`, and `jsonschema`. You do not have root access, so install them locally or via pip.

2. **Data Ingestion & Querying**:
   - An RDF file in Turtle format is located at `/home/user/infrastructure.ttl`. It contains the infrastructure graph.
   - Use `rdflib` and **SPARQL** to extract the following information:
     - Databases (entities of type `ex:Database`) that are missing backups (have property `ex:needsBackup "true"^^xsd:boolean`). Also extract their `ex:dbSize` (integer).
     - Storage Nodes (entities of type `ex:StorageNode`) and their `ex:availableCapacity` (integer).
     - Network Links (entities of type `ex:NetworkLink`) containing `ex:source`, `ex:target`, and `ex:latency` (integer). *Note: Network links in this infrastructure are bidirectional. If a link exists from A to B, traffic can flow from B to A with the same latency.*

3. **Graph Traversal & Routing**:
   - For each database that needs a backup, use the extracted network links to build a routing graph (e.g., using `networkx`).
   - Calculate the shortest path (minimizing total latency) from the database to a Storage Node that has an `ex:availableCapacity` **strictly greater than or equal to** the database's `ex:dbSize`.
   - *Note: Multiple databases can be routed to the same storage node without deducting from its capacity for this planning phase.*

4. **Schema Validation & Output**:
   - Your output must be an array of JSON objects, sorted in ascending alphabetical order by `database_id`.
   - The output must be validated against the JSON schema located at `/home/user/output_schema.json` before writing.
   - Write the validated JSON to `/home/user/backup_routing_plan.json`.

Ensure your script is robust and correctly handles the bidirectional nature of the network links during pathfinding. Run your script to generate the final output file.