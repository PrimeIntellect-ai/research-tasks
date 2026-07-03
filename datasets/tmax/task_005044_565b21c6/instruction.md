You are a data engineer tasked with building an ETL pipeline to process and transform relational graph data into a document format while performing analytical aggregations.

You are provided with an SQLite database at `/home/user/network.db`. This database contains two tables:
1. `nodes` (node_id INTEGER PRIMARY KEY, label TEXT, category TEXT)
2. `edges` (source_id INTEGER, target_id INTEGER, weight INTEGER)

Write a Bash script at `/home/user/etl_pipeline.sh` that performs the following operations using the `sqlite3` command-line tool:

1. **Index Strategy**: Create a composite index named `idx_source_weight` on the `edges` table covering `source_id` and `weight` (descending) to optimize window function queries.
2. **Window Functions & Filtering**: Create a new table named `top_edges` in the same database. This table should contain only the top 2 outgoing edges (highest `weight`) for each `source_id`. If there is a tie in weight, break the tie by ordering `target_id` ascending.
3. **Cross-Representation Mapping**: Extract the graph data (all nodes, but ONLY the edges from the `top_edges` table) and format it as a single JSON object. Save this JSON output to `/home/user/graph.json`. 
   The JSON must have this exact structure:
   `{"nodes":[{"id":1,"label":"N1","category":"A"},...],"edges":[{"source":1,"target":2,"weight":15},...]}`
   (Hint: You can use SQLite's built-in `json_object` and `json_group_array` functions to generate this directly from queries).
4. **Analytical Aggregation**: Calculate the sum of the weights of ALL original edges (from the `edges` table, not just top_edges) grouped by the `category` of the **source** node. Write the results to `/home/user/metrics.txt` with one line per category, sorted alphabetically by category name. 
   Format of each line: `Category: [category_name], Total Weight: [sum_weight]`

Make sure your script `/home/user/etl_pipeline.sh` is executable (`chmod +x`) and run it so the output files are generated.