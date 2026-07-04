You are a Database Reliability Engineer (DRE) responsible for the disaster recovery strategy of a complex microservices architecture. To ensure a successful system restore, you need to identify the most critical database backups—those that the highest number of other databases depend on.

You have exported the dependency graph of your databases from your graph database (using a Cypher query) into a JSON file located at `/home/user/backup_query_result.json`. The graph edges represent a `DEPENDS_ON` relationship (i.e., the `source` database cannot function without the `target` database being restored first).

Your task is to write a C++ program named `/home/user/analyze_backups.cpp` that performs the following:
1. Parses the `/home/user/backup_query_result.json` file. A popular single-header JSON library is already provided for you at `/home/user/json.hpp` (nlohmann/json).
2. Performs a basic graph centrality analysis by calculating the in-degree (number of incoming `DEPENDS_ON` edges) for each `target` database.
3. Sorts the databases based on their in-degree in descending order. If two databases have the same in-degree, sort them alphabetically in ascending order by their name.
4. Implements pagination/filtering by isolating only the Top 3 most critical databases.
5. Writes these top 3 databases to `/home/user/critical_backups.log` in the exact format: `[RANK]. [DB_NAME] - [COUNT] dependencies`

Example output format for `critical_backups.log`:
1. users_db - 5 dependencies
2. catalog_db - 3 dependencies
3. auth_db - 3 dependencies

Compile your program using standard `g++` (e.g., `g++ -std=c++11 analyze_backups.cpp -o analyze_backups`), run it, and ensure the log file is generated successfully.