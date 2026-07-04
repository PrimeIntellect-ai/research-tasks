You are assisting a researcher who is organizing a complex dataset of conceptual dependencies. The data is stored in an SQLite database located at `/home/user/concepts.db`. The researcher has forgotten the exact schema, but knows it contains a set of concepts and a set of directional, weighted relationships (dependencies) between them.

Your task has three parts:

1. **Reverse Engineer and Optimize**:
   Explore `/home/user/concepts.db` to determine its table structure. The database currently lacks proper indexing, making relationship lookups slow.
   Determine the optimal index strategy to quickly find all outgoing relationships and their weights for a given concept. Write the SQL statement(s) to create these indexes and save them to `/home/user/optimize.sql`.

2. **Graph Traversal Script**:
   Write a Python script at `/home/user/pathfinder.py` that computes the shortest weighted path between two concepts.
   - The script must take exactly two command-line arguments: the starting concept ID and the ending concept ID.
   - Example usage: `python3 /home/user/pathfinder.py <start_id> <end_id>`
   - It must query the database dynamically to traverse the graph (e.g., using Dijkstra's algorithm).
   - For security and performance, all database queries inside the script must use **parameterized queries**.
   - The script should print ONLY the shortest path as a comma-separated list of IDs (e.g., `1,5,9,10`).

3. **Execution**:
   - Run your script to find the shortest path from concept ID `15` to concept ID `85`.
   - Save the exact printed output to `/home/user/path.txt`.