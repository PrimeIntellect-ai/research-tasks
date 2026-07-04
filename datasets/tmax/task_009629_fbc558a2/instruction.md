You are a Database Reliability Engineer responsible for ensuring the integrity of graph database backups. Your current task is to verify a recent uncompressed snapshot of a graph database before it is approved for archiving. The backup system uses a lightweight CSV-based format.

The backup consists of two files located in `/home/user/backup/`:
1. `/home/user/backup/nodes.csv` - Contains the nodes with columns `id,label`.
2. `/home/user/backup/edges.csv` - Contains directed edges with columns `source,target,type`.

To verify the structural integrity and validate the schema relationships of this backup, you need to write a custom C++ analysis tool. Standard graph databases are not available in this environment, so you must implement the in-memory graph index and query logic from scratch.

Please complete the following steps:
1. Create a C++ program at `/home/user/workspace/verify_backup.cpp`.
2. The program must read the `nodes.csv` and `edges.csv` files.
3. Perform the following graph analytics and schema pattern matching:
   - **Analytic A (Centrality):** Find the node `id` with the highest out-degree (the highest number of outgoing edges). If there is a tie, select the node with the lowest numeric `id`.
   - **Analytic B (Pattern Matching):** Count the exact number of occurrences of the following topological schema pattern:
     `(Node with label 'User') -[Edge type 'KNOWS']-> (Node with label 'User') -[Edge type 'LIKES']-> (Node with label 'Post')`
4. Write the results of these two analytics to a JSON file at `/home/user/workspace/report.json` in the exact following format:
   ```json
   {
     "highest_out_degree_node": <integer_id>,
     "pattern_match_count": <integer_count>
   }
   ```
5. Compile your C++ program using standard `g++` and execute it to generate the `report.json` file.

Do not use any external non-standard C++ libraries (e.g., Boost). Standard library (`<vector>`, `<unordered_map>`, `<string>`, etc.) is fully permitted. Assume the CSV files have a header row and are strictly comma-separated without quoted strings.