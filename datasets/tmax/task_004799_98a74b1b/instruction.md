You are a database administrator tasked with optimizing and analyzing a system dependency graph for a legacy platform. 

You have been provided an SQLite database file at `/home/user/system_graph.db`. Unfortunately, the original schema documentation is lost. 

Your task is to:
1. Reverse engineer the data model of the SQLite database to identify the tables and columns that store entities and their relationships.
2. Identify the relation type that represents a "DEPENDS_ON" relationship.
3. Write a C++ program at `/home/user/analyze_graph.cpp` that connects to this database and computes the out-degree centrality specifically for the "DEPENDS_ON" relationship.
4. Materialize this graph projection and identify the top 3 entities with the highest out-degree (i.e., the entities that depend on the most other distinct entities).
5. Compile and run your C++ program. Ensure it writes exactly the names of these top 3 entities to `/home/user/result.txt`, one name per line. If there is a tie in out-degree, sort the tied entity names alphabetically in ascending order.

To solve this, you will need to inspect the database, write the C++ code utilizing the `sqlite3` C/C++ library, compile it (e.g., using `g++`), and output the final text file.

The resulting `/home/user/result.txt` should contain only the names of the 3 entities, like so:
Entity_Name_1
Entity_Name_2
Entity_Name_3