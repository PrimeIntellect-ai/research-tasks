I am a researcher organizing a massive collection of citation network datasets. These datasets are stored as SQLite databases, but some of them have been corrupted by data-entry errors resulting in impossible citation cycles (e.g., Paper A cites Paper B, which cites Paper C, which cites Paper A). 

I need an automated tool written in C to analyze these database files, project the graph, and filter out the corrupted datasets.

Here is your task:

1. **Fix the SQLite Build:** 
   I have vendored the SQLite source code in `/app/sqlite-src`. It contains a `build.sh` script to compile the library (`libsqlite3.a`). However, a previous assistant accidentally introduced a configuration flag in the build script that breaks support for hierarchical and recursive graph queries. You need to identify the issue in `/app/sqlite-src/build.sh`, fix it, and build the SQLite library.

2. **Develop the Graph Analyzer:**
   Write a C program at `/home/user/checker.c` that links against your fixed `/app/sqlite-src/libsqlite3.a`. 
   The program must accept exactly one command-line argument: the absolute path to a SQLite database file.
   
   Each database contains a single table:
   `CREATE TABLE citations (source_id INT, target_id INT);`
   
   Your C program must:
   - Connect to the provided SQLite database.
   - Use a parameterized query or a **Recursive CTE** (Common Table Expression) to traverse the citation graph.
   - Perform schema analysis and relationship mapping to detect if there is *any* cycle in the graph. 
   - Print exactly `CLEAN` to standard output and exit with status `0` if the graph is a valid Directed Acyclic Graph (DAG) with zero cycles.
   - Print exactly `EVIL` to standard output and exit with status `1` if the graph contains one or more cycles.

3. **Verify:**
   I have placed a set of test datasets in two directories:
   - `/home/user/corpora/clean/` (Valid DAGs)
   - `/home/user/corpora/evil/` (Corrupted graphs with cycles)
   
   Compile your C program to `/home/user/checker`. Ensure it correctly classifies every database in those directories.