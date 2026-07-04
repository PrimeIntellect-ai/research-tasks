You are a Database Reliability Engineer. We maintain a system of incremental backups represented as directed acyclic graphs (DAGs) in SQLite databases. A recent storage glitch corrupted several of our backup metadata databases, introducing cyclic dependencies in the incremental backup chains. If our automated restore system encounters a cycle, it will infinite-loop and crash.

Your task is to build a cycle-detecting validation tool in C that acts as a filter. 

**Step 1: Fix the Vendored SQLite Library**
We have vendored the source code for `sqlite-amalgamation-3430200` in `/app/sqlite-amalgamation/`. However, the provided `Makefile` is broken due to a deliberate perturbation (a typo in the source file name). 
1. Fix the `Makefile` so that running `make` successfully produces `sqlite3.o`. 

**Step 2: Build the Backup Validator**
Write a C program at `/home/user/backup_validator.c` and compile it to `/home/user/backup_validator`. It must link against the `sqlite3.o` you just built.
1. The program must accept exactly one command-line argument: the path to a SQLite database file.
2. The database contains a single table: `incremental_backups(id INTEGER PRIMARY KEY, parent_id INTEGER)`. A root backup has `parent_id IS NULL`.
3. Your C program must use the SQLite C API to traverse the hierarchy starting from the backup with `id = 100`. It must follow the `parent_id` references upward to the root.
4. **Validation Logic:** You must detect if the chain starting from `id = 100` forms a valid path to a root (a valid DAG path) or if it gets trapped in a cycle (e.g., A -> B -> C -> A). You can achieve this using a recursive CTE with cycle detection, or by manually traversing and keeping track of visited nodes in C.
5. If the chain is clean and successfully reaches a root node without cycles, the program must print exactly `ACCEPT` to standard output and exit with status code `0`.
6. If the chain contains a cycle, the program must print exactly `REJECT` to standard output and exit with status code `1`.

We have provided two directories containing test databases:
* `/app/corpora/clean/` - Contains uncorrupted databases (valid chains).
* `/app/corpora/evil/` - Contains corrupted databases (cyclic chains).

To complete the task, ensure your binary `/home/user/backup_validator` compiles cleanly and correctly classifies every database in the two corpora.