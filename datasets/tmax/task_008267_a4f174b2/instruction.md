You are a data engineer tasked with building an ETL pipeline step that extracts communication patterns from an SQLite database.

We have an SQLite database located at `/home/user/data.db`. It contains a table named `communications` with the schema:
`sender INT, receiver INT, time INT`

There is a known issue with the database: the index `idx_time` is corrupted. When querying the table, you MUST bypass this index by using the `NOT INDEXED` clause in your SQL query (e.g., `FROM communications NOT INDEXED`), otherwise you may retrieve stale or duplicated rows.

Your task is to write a C++ program at `/home/user/find_pattern.cpp` that reads the data from this SQLite database and finds all directed communication cycles of length 3 (triangles) where the communication happens in strictly increasing chronological order. 
Specifically, find all sequences of nodes (A, B, C) such that:
1. A sent a message to B at time t1
2. B sent a message to C at time t2
3. C sent a message to A at time t3
4. t1 < t2 < t3

Your C++ program should:
1. Connect to `/home/user/data.db`.
2. Retrieve the valid rows, making sure to avoid the corrupted index.
3. Build a graph representation in memory.
4. Discover all cycles matching the temporal condition described above.
5. Output the discovered cycles to a file `/home/user/cycles.txt`.

The output format for `/home/user/cycles.txt` must be one cycle per line, formatted as a comma-separated list of the three nodes: `node1,node2,node3`.
For each cycle, rotate the sequence so that the smallest node ID is first (e.g., if the cycle is 3->1->2, write `1,2,3`). 
Sort the lines in the output file lexicographically.

You can install any necessary C++ libraries (e.g., `libsqlite3-dev`) via `apt-get` if they are not already installed, and compile your code using `g++`. 
Once your program finishes, the file `/home/user/cycles.txt` must contain the exact correct cycles.