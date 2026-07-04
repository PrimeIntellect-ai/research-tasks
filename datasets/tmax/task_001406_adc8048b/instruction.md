I am a researcher trying to organize an old dataset left by a former colleague. The data is stored in an SQLite database located at `/home/user/data/experiment.db`. Unfortunately, there is no documentation for the database schema, and the table and column names are obfuscated (e.g., `t_001`, `t_002`, etc.).

I know the database contains graph data representing experimental entities and the interactions between them. One table holds the entities (with an ID, a label, and a category), and another holds the interactions (with a source ID, a destination ID, and an interaction strength value).

I need you to:
1. Reverse engineer the schema of `/home/user/data/experiment.db` to identify the entity and interaction tables.
2. Write a C++ program at `/home/user/process.cpp` that reads this database using the SQLite3 C API.
3. The C++ program must project a specific subgraph:
   - Only include entities where the category is exactly the string `'A'`.
   - Only include interactions where the strength value is strictly greater than `5.0`.
   - An interaction is only valid if *both* its source and destination entities are in category `'A'`.
4. The C++ program should materialize this subgraph and export the results to two CSV files in `/home/user/`:
   - `/home/user/nodes.csv` with the format `id,label,degree`. The `degree` should be the number of valid interactions connected to that entity (treating interactions as undirected for the degree calculation). Include all entities of category `'A'`, even if their degree is 0. Sort the rows by `id` in ascending order.
   - `/home/user/edges.csv` with the format `src,dst,value`. Only include the valid interactions. Sort the rows by `src` ascending, then `dst` ascending.

Compile your C++ program to `/home/user/process` and run it to produce the CSV files. You can use standard C++17 libraries and `sqlite3.h`.