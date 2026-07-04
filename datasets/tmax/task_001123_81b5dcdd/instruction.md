I am a researcher trying to organize a massive collection of scientific datasets. I want to find the shortest "collaboration path" between different datasets, where a connection exists if two datasets share at least one author. 

I wrote a C++ program (`/home/user/graph_search.cpp`) that uses SQLite3 to do a Breadth-First Search (BFS) on my database (`/home/user/research_data.db`) to find the shortest path between two datasets by their titles. However, the program is running out of memory and taking forever. I suspect there is a severe bug in the SQL query fetching the neighboring datasets—it seems to be doing an implicit cross join and returning millions of incorrect adjacent nodes. Furthermore, the query doesn't use parameterized queries properly, making it vulnerable and slow, and the database has absolutely no indexes!

Your task:
1. **Reverse Engineer Data Model**: Inspect `/home/user/research_data.db` to understand the schema for datasets, authors, and their relationships.
2. **Fix the C++ Code**: Edit `/home/user/graph_search.cpp`. Fix the SQL query that fetches adjacent datasets. Two datasets are adjacent if they share at least one author. Ensure the query strictly prevents implicit cross joins. Update the code to use **proper SQLite parameterized queries** (`sqlite3_bind_*`) instead of string formatting for the inputs.
3. **Design Index Strategy**: Create a file `/home/user/optimize.sql` containing the SQL commands to create the optimal indexes for your new query. Apply this script to the database.
4. **Compile and Run**: Compile the C++ program (e.g., `g++ -O3 /home/user/graph_search.cpp -o /home/user/graph_search -lsqlite3`).
5. **Output**: Run your fixed program to find the shortest path between the dataset titled `"Quantum Entanglement Set"` and `"Macroscopic Superposition Set"`. Write the exact output (which the C++ program prints as a comma-separated list of dataset titles representing the path) to `/home/user/path_result.txt`.

**Expected output format in `/home/user/path_result.txt`:**
Dataset Title 1,Dataset Title 2,Dataset Title 3,...