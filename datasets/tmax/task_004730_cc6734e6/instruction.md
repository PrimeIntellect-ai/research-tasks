You are a database administrator optimizing a legacy, bash-based graph database engine. 

A specific tool in the suite, vendored at `/app/sh-graph-query-1.0`, has a bug. The script `/app/sh-graph-query-1.0/bin/query_edges.sh` is supposed to take a single argument (`<node_id>`), read from a file named `edges.csv` in the current directory (format: `source_id,target_id,weight`), and return all outgoing edges for that `node_id`. 

The output must be formatted as `target_id,weight` (one per line) and must be sorted numerically by `target_id` (ascending), and then by `weight` (ascending). 

Currently, the script returns incorrect results—often dumping the entire edge table—due to a logical bug in its `awk` filtering that acts like an implicit cross join (ignoring the filter condition). 

Your task is to fix the script `/app/sh-graph-query-1.0/bin/query_edges.sh` in-place so that it correctly filters the edges for the given `node_id` and sorts the results exactly as specified. 

Do not change the script's invocation method (it must continue to accept the `node_id` as `$1`). Assume `edges.csv` will be present in the directory where the script is executed.