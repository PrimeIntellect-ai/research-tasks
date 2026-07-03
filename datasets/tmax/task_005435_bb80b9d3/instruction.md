You are a data analyst investigating a set of financial transactions. You have been given two CSV files with obfuscated column names in `/home/user/data/`:
1. `/home/user/data/entity_info.csv`
2. `/home/user/data/events.csv`

Your task is to reverse-engineer the data model, extract a specific graph projection, optimize it for querying, and output the top influencers.

Please write and execute a Bash script at `/home/user/analyze.sh` that does the following:
1. Creates a new SQLite database at `/home/user/graph.db`.
2. Imports the two CSV files into the database. You will need to infer the foreign key relationships (one file contains entity profiles with an ID and a string handle, the other contains event records linking a sender entity, a receiver entity, and an event value).
3. Materializes a graph projection by creating a new table named `projected_edges`. This table should contain distinct `(source_handle, target_handle)` pairs representing directed edges where:
   - The event value is strictly greater than 50.
   - Self-loops (where the sender and receiver are the same entity) are excluded.
   - Duplicate edges between the same two entities are reduced to a single distinct edge.
4. Optimizes the query plan by creating an index named `idx_source` on the `source_handle` column of the `projected_edges` table.
5. Queries the `projected_edges` table to find the top 3 entities with the highest out-degree (number of unique targets they connected to). If there is a tie in out-degree, sort alphabetically by the handle ascending.
6. Writes the top 3 results to `/home/user/top_nodes.txt` strictly in the following format:
   `Handle: <handle>, OutDegree: <degree>`

You must run the script and ensure both `/home/user/graph.db` and `/home/user/top_nodes.txt` are generated successfully.