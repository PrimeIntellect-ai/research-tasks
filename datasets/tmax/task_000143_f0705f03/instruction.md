You are acting as a Database Administrator managing a custom graph database system. The system uses a proprietary compiled query engine that translates a custom Graph Query Language (GQL) into SQLite recursive Common Table Expressions (CTEs). 

Recently, we discovered that one of our SQLite indexes, `idx_stale_edges` on the `graph.db` database, has become corrupted and occasionally returns stale rows. Rebuilding the index requires downtime we cannot currently afford. We have a safe index, `idx_safe_edges`, but the query engine sometimes generates SQL query plans that still favor the corrupted index depending on the query parameters.

Your task is to create a classification script that intercepts GQL queries and rejects those that would hit the corrupted index.

**System Details:**
*   Database: `/app/graph.db`
*   Query Compiler: `/app/graph_compiler` (a stripped, pre-compiled binary). 
    *   Usage: `/app/graph_compiler < query.gql` outputs the compiled SQLite query to `stdout`.
*   You must write an executable script at `/home/user/filter.sh` (you may use Python or Bash, but it must be runnable via exactly `/home/user/filter.sh <path_to_gql_file>`).
*   Your script must:
    1. Read the provided `.gql` file.
    2. Pass it through `/app/graph_compiler` to get the generated SQL.
    3. Generate the SQLite Query Plan for this SQL against `/app/graph.db`.
    4. If the query plan relies on `idx_stale_edges`, the script must **reject** the query by exiting with code `1`.
    5. If the query plan avoids the corrupted index (e.g., uses `idx_safe_edges` or performs a standard table scan), the script must **accept** the query by exiting with code `0`.
*   Ensure your script does not execute the actual query or modify the database—only interpret the query plan.

We have provided a set of test files you can use to verify your logic if you wish, but the automated grader will test your script against a hidden set of clean and evil queries.