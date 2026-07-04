As a compliance officer, I am auditing our corporate registry and transaction logs to detect potential regulatory evasion and circular asset locking (which can cause transaction deadlocks). 

I have exported our internal records into an RDF Turtle file located at `/home/user/corporate_graph.ttl`.

Your task is to write a Python script that uses the `rdflib` library to query this knowledge graph using SPARQL. 

Specifically, you need to find all instances of a specific compliance violation pattern:
A company (?a) owns another company (?b), and (?b) owns a third company (?c), but (?c) has executed a transaction with the original company (?a). 

The relationships in the RDF file use the namespace `http://example.org/audit/` with the predicates `owns` and `transactsWith`.

Your Python script should:
1. Parse `/home/user/corporate_graph.ttl`.
2. Execute a SPARQL query to find all combinations of `?a`, `?b`, and `?c` that match this exact pattern.
3. Extract just the local names (the part after the namespace, e.g., "CorpA") of the entities.
4. Write the results to `/home/user/violations.csv`.

Format requirements for `/home/user/violations.csv`:
- No header row.
- Each line should be formatted strictly as: `a_name,b_name,c_name`
- Sort the lines alphabetically by the `a_name`, then `b_name`, then `c_name`.

You may need to install `rdflib` first. Save your script wherever you like, but ensure the final output file is generated exactly at `/home/user/violations.csv`.