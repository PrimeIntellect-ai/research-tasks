You are acting as a database administrator tasked with analyzing a transaction locking graph to detect deadlocks. 

A system periodically dumps its lock manager state into an RDF Knowledge Graph in Turtle format. The graph contains `Transaction` and `Resource` entities. 
The relationships are defined by two predicates:
- `ex:holds`: A transaction currently holds an exclusive lock on a resource.
- `ex:waitsFor`: A transaction is waiting to acquire a lock on a resource.

A transaction $A$ is effectively waiting for a transaction $B$ if $A$ `waitsFor` a resource that $B$ `holds`.
A deadlock occurs when there is a cyclic dependency of transactions waiting for each other (e.g., $A$ waits for $B$, and $B$ waits for $A$; or $A$ waits for $B$, $B$ waits for $C$, and $C$ waits for $A$).

Your task is to:
1. Write a Python script `/home/user/detect_deadlocks.py` that parses `/home/user/locks.ttl` using the `rdflib` library. You may need to install this library.
2. Write and execute a SPARQL query within the script to identify all transactions that are part of a deadlock cycle of length 2 or length 3.
3. Extract the local names of the deadlocked transactions (e.g., if the URI is `http://example.org/T1`, extract `T1`).
4. Output the unique, alphabetically sorted list of these deadlocked transaction IDs as a JSON array to `/home/user/deadlocks.json`.

Ensure your script runs successfully and writes the correctly formatted JSON file. 

Example expected output format for `/home/user/deadlocks.json`:
```json
[
  "T1",
  "T2",
  "T9"
]
```