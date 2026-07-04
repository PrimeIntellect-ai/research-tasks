You are a database reliability engineer managing backups for a specialized graph database. Recently, a corrupted index caused the database to export stale and conflicting rows into our daily graph dump. 

You have been provided with the raw, corrupted dump at `/home/user/graph_backup.csv`. The file is a CSV without a header, where each line represents an edge in the graph in the format:
`subject,predicate,object,timestamp` (where timestamp is an integer).

Due to the corruption, entities in the graph have multiple `current_status` edges with different timestamps. In reality, a subject can only have one valid `current_status` at a time.

Your task is to write a Go program at `/home/user/clean_graph.go` that processes this dump and writes a cleaned graph projection to `/home/user/clean_backup.csv`. 

The Go program must perform the following knowledge graph pattern matching and filtering:
1. **Resolve Stale States:** For any given `subject`, if there are multiple edges with the predicate `current_status`, keep *only* the edge with the strictly highest `timestamp`. Discard all older `current_status` edges for that subject.
2. **Project the Subgraph:** The final output graph must ONLY contain:
   a) The resolved, valid `current_status` edges for all subjects.
   b) Any edge with the predicate `manages` (e.g., `UserX,manages,NodeY,timestamp`) BUT ONLY IF the object of the `manages` relation (`NodeY`) has a resolved, valid `current_status` of exactly `ACTIVE`. If the target node's latest status is anything else (or if it has no status), the `manages` edge must be discarded.
3. **Format:** Write the projected edges to `/home/user/clean_backup.csv` in the exact same comma-separated format (`subject,predicate,object,timestamp`). 
4. **Ordering:** Sort the lines in the output file lexicographically by the entire line string to ensure deterministic verification.

Run your Go program to generate `/home/user/clean_backup.csv`.