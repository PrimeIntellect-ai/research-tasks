You are a database administrator optimizing query execution and securing our internal analytics cluster. Recently, analysts have been submitting poorly formed queries that contain accidental implicit cross joins (Cartesian products without `ON` or `WHERE` clauses) and recursive CTE bombs, leading to database lockups.

We need a sanitization filter written in C that rejects these "evil" queries while allowing valid, optimized queries through.

Part 1: Fix the Vendored Package
We rely on a custom vendored version of a lightweight SQL formatting and parsing utility called `sql-parser-c` located at `/app/sql-parser-c/`. 
However, the package is currently broken. A recent internal patch introduced a deliberate perturbation: the `Makefile` has a malformed `CFLAGS` environment variable definition, and `src/parser.c` is missing a critical `#include` for standard I/O, which causes the build to fail.
1. Fix the `Makefile` and `src/parser.c` so that running `make` successfully compiles the `libsqlparser.a` static library.
2. Verify the fix by ensuring the known-good code path (`make test`) passes.

Part 2: Build the Query Sanitizer
Write a C program at `/home/user/query_sanitizer.c` that statically analyzes a given SQL query file.
The program must:
1. Read a SQL query from a file (the file path is passed as the first command-line argument).
2. Detect implicit cross joins (e.g., `FROM tableA, tableB` without an accompanying `WHERE` clause bridging them, or `CROSS JOIN` explicitly used without a limit).
3. Detect recursive CTEs lacking a termination limit (e.g., `WITH RECURSIVE` that does not contain a `LIMIT` clause in the final `SELECT`).
4. Print `ACCEPT` to standard output and exit with code 0 if the query is safe.
5. Print `REJECT` to standard output and exit with code 1 if the query contains these dangerous patterns.

Part 3: Adversarial Verification
We have provided two directories containing query logs:
- `/app/corpora/clean/`: Contains 50 well-formed SQL queries.
- `/app/corpora/evil/`: Contains 50 resource-exhaustion and cross-join queries.

Your compiled program `/home/user/query_sanitizer` must output `REJECT` for every file in the `evil` corpus and `ACCEPT` for every file in the `clean` corpus. 

Compile your program linking against the fixed `/app/sql-parser-c/libsqlparser.a`. Once complete, create a log file at `/home/user/verification.log` containing the text "SANITIZER BUILD COMPLETE".