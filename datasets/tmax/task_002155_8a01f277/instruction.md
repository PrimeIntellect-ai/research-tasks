You are acting as a Database Administrator tasked with optimizing and querying a relational database that models a knowledge graph of users, their skills, and their project collaborations. 

You have been provided with an SQLite database file at `/home/user/knowledge_graph.db`. You do not have the exact schema, so you must first reverse-engineer the data model by inspecting the database.

Your task is to write a Python script at `/home/user/query_optimizer.py` that queries this database to find pairs of users who have collaborated on projects AND share a specific skill. 

Your script must meet the following requirements:
1. It must accept exactly three command-line arguments: `<skill_name>` (string), `<limit>` (integer), and `<offset>` (integer).
   Example: `python3 /home/user/query_optimizer.py "Python" 10 0`
2. It must use a parameterized SQL query to prevent SQL injection and ensure query execution plan optimization.
3. The query must find pairs of users (User A and User B) who:
   - Both possess the skill specified by `<skill_name>`.
   - Have worked on at least one project together.
4. To avoid duplicate pairs (e.g., A-B and B-A) and self-pairs (A-A), enforce that User A's name is strictly less than User B's name alphabetically.
5. The results must be grouped and sorted by:
   - The number of shared projects between the two users (Descending order).
   - User A's name (Ascending alphabetical order).
   - User B's name (Ascending alphabetical order).
6. Apply the pagination parameters (`limit` and `offset`) to the final sorted results.
7. The script must write the final output to `/home/user/optimized_results.json` as a JSON array of objects. Each object must exactly match this structure:
   ```json
   [
     {
       "user_a": "Alice Smith",
       "user_b": "Bob Jones",
       "shared_projects_count": 3
     }
   ]
   ```

Ensure your query uses complex joins efficiently rather than doing the processing in Python. The database contains indexes that will make this query performant if written correctly. Do not modify the database.