You are assisting a researcher in organizing and analyzing a citation network dataset. The dataset is stored in an SQLite database located at `/home/user/citation_network.db`. 

The database contains two tables:
1. `papers` (`id` INTEGER PRIMARY KEY, `title` TEXT, `year` INTEGER)
2. `citations` (`source_id` INTEGER, `target_id` INTEGER) - Represents a directed edge from `source_id` to `target_id`.

The researcher has encountered several issues and needs your help to clean the data, optimize the queries, and extract graph metrics.

**Your Tasks:**

1. **Fix Database Integrity:** The database currently has a corrupted index named `idx_citations_target` on the `citations` table. Due to a bug during a previous bulk import, this index is out of sync and returns stale/phantom rows when queried. You must fix this by dropping the corrupted index and recreating it (or running the appropriate SQLite command to rebuild indexes).
2. **Query Optimization:** The researcher frequently queries for citations to specific papers, but the queries are slow. Ensure that optimal indexes exist for both `source_id` and `target_id` on the `citations` table to optimize graph traversal.
3. **Graph Analytics Script:** Write a Bash script at `/home/user/export_graph_metrics.sh` that calculates a specific graph metric for the network. 
   - We define **Recent In-Degree** as the total number of citations a paper has received specifically from papers published in the year **2018 or later**.
   - Your script must query the `citation_network.db` database using `sqlite3` and output the top 5 papers with the highest Recent In-Degree.
   - If there is a tie in Recent In-Degree, break the tie by sorting the paper `id` in **ascending** order.
   - The script must output **only** a valid JSON array of objects to standard output (STDOUT), matching this exact structure:
     ```json
     [
       {"id": 105, "title": "Paper Title A", "recent_in_degree": 42},
       {"id": 42, "title": "Paper Title B", "recent_in_degree": 38}
     ]
     ```
   - Do not print any other text, warnings, or formatting characters outside the JSON array.

Ensure your Bash script is executable (`chmod +x /home/user/export_graph_metrics.sh`).