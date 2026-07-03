I am a bioinformatics researcher organizing several large environmental and genomic datasets. We are building a web portal where external scientists can submit SQL queries to aggregate and analyze our data. However, we need a strict query validator to prevent destructive operations and restrict access to sensitive tables.

I have started setting this up, but I need your help to complete it. 

First, we are using a custom-compiled version of SQLite to ensure specific extensions and security features are enabled. The source code for SQLite (amalgamation version 3.43.2) is located in `/app/sqlite/`. I tried to write a `Makefile` for it, but the compilation fails or disables the authorization features I need. You need to fix the `Makefile` in `/app/sqlite/` so that SQLite compiles correctly as a static library (`libsqlite3.a`) with authorization features enabled.

Second, you must write a C program at `/home/user/validator.c` (and compile it to `/home/user/validator`) that acts as our query filter. 
The program must:
1. Accept exactly one command-line argument: the path to a file containing a SQL query.
2. Open an in-memory SQLite database (`:memory:`).
3. Create the following dummy schema in the database so queries can be parsed:
   `CREATE TABLE datasets (id INTEGER, name TEXT);`
   `CREATE TABLE measurements (id INTEGER, dataset_id INTEGER, value REAL);`
   `CREATE TABLE restricted_metadata (id INTEGER, patient_name TEXT);`
4. Read the SQL query from the provided file.
5. Analyze the query to determine if it should be allowed.
6. Print exactly `ACCEPT` to standard output if the query is safe, or `REJECT` if it is unsafe. It should exit with code 0 in both cases.

Rules for Safe/Unsafe Queries:
- The query MUST be strictly read-only (e.g., standard `SELECT` statements, including complex joins, CTEs, and aggregations are allowed).
- The query MUST NOT modify the database (no `INSERT`, `UPDATE`, `DELETE`, `DROP`, `CREATE`, `ALTER`, `PRAGMA`, etc.).
- The query MUST NOT attempt to access the `restricted_metadata` table in any way.
- If the query has a syntax error or accesses tables that do not exist in the dummy schema, print `REJECT`.

To test your program, I have provided two directories of queries:
- `/app/corpora/clean/` contains valid, safe analytical queries that must be ACCEPTED.
- `/app/corpora/evil/` contains unsafe queries, destructive operations, and attempts to access the restricted table. These must be REJECTED.

Please fix the SQLite compilation, write the C program, link it against your fixed `libsqlite3.a`, and ensure your validator perfectly classifies the corpora.