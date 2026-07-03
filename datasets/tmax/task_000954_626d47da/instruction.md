I am a data analyst working with several CSV datasets representing graph edge lists. I have a vendored C utility package called `libcsv-graph` located at `/app/libcsv-graph` that is supposed to help me process these files, compute weighted in-degree centralities, and output paginated results.

Unfortunately, the vendored tool is broken. When I try to use it, it doesn't compile correctly, and even when I manually compile it, the sorting logic and pagination seem to be completely off.

Here is what I need you to do:
1. Navigate to `/app/libcsv-graph` and inspect the source code and Makefile. 
2. Fix the `Makefile` so that running `make` correctly builds the executable binary named `in_degree` (it currently has a typo/configuration error that prevents the CLI tool from linking properly).
3. Fix the logic in `in_degree.c`. The program takes 4 arguments: `<input_csv>` `<min_weight_threshold>` `<limit>` `<offset>`.
   - The CSV format is `source_node,target_node,weight` (all integers, no header).
   - It needs to aggregate the total weighted in-degree (sum of weights of incoming edges) for each unique `target_node`.
   - It must filter out any `target_node` whose total weighted in-degree is strictly less than `<min_weight_threshold>`.
   - It must sort the remaining target nodes in *descending* order of their in-degree (and ascending order of `target_node` ID in case of a tie).
   - Finally, it must print a paginated view of the sorted results using the `<limit>` (number of items to display) and `<offset>` (number of items to skip).
   - The output format must be strictly one node per line: `Node: <node_id>, In-Degree: <total_weight>`.

You do not need to worry about the underlying input files being malformed (they will strictly contain 3 comma-separated integers per line). Fix the package so that running `./in_degree` perfectly matches the expected aggregation, sorting, filtering, and pagination behavior.

Please compile the fixed version using `make` leaving the final executable at `/app/libcsv-graph/in_degree`.