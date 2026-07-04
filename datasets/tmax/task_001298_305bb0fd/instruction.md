As a compliance officer, I am conducting an audit of our internal access management systems. Our legacy access verification tool is a compiled, stripped binary located at `/app/access_oracle`. 

This binary takes two arguments: an `<EntityID>` and a `<TargetID>`, and outputs either `GRANTED` or `DENIED` to standard output. It determines access by checking if there is a valid directed path from the `<EntityID>` to the `<TargetID>` using the edge list provided in `/app/access_graph.tsv` (where each line is `Source<TAB>Target`).

Because the binary is a black box, it fails our new transparency requirements for compliance. I need you to write a Bash script located at `/home/user/audit_query.sh` that takes the exact same two arguments (`<EntityID>` and `<TargetID>`) and replicates the behavior of `/app/access_oracle` exactly. 

You should use your knowledge of recursive data querying to accomplish this. You may embed SQLite3 queries (using recursive CTEs) within your Bash script, or use standard Linux text processing pipelines or inline scripting (like Python) inside the Bash script, but the entry point MUST be `/home/user/audit_query.sh`.

Requirements:
- The graph file `/app/access_graph.tsv` contains no headers.
- Your script must output `GRANTED` if there is a directed path from `<EntityID>` to `<TargetID>` (path length >= 1), and `DENIED` otherwise.
- Output must be exactly the string, followed by a newline.
- You can test your script against the `/app/access_oracle` binary to ensure it matches.

Please create the `/home/user/audit_query.sh` script.