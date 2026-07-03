You are acting as a Data Engineer managing an ETL pipeline that translates proprietary graph queries into SQL for execution on our analytical warehouse. 

We use an internal C++ tool called `libcypher2sql` (vendored at `/app/libcypher2sql-0.5.0/`) to compile our simple graph patterns into complex SQL statements with window functions and aggregations. Unfortunately, there are two major issues:

1. **Build Failure:** After a recent system update, the package no longer compiles. We suspect a minor misconfiguration in the build system (`Makefile`). You need to fix the build so that running `make` successfully produces the `cypher2sql` executable.
2. **Implicit Cross Join Bug:** Even when manually compiled, the tool generates broken SQL for multi-hop graph patterns. For example, when parsing an input like `MATCH node:User edge:Follows node:User`, it generates `SELECT * FROM User n0, Follows e0, User n1;`. This implicit cross join causes our database to hang. It should be generating proper join conditions: `SELECT * FROM User n0 JOIN Follows e0 ON n0.id=e0.src JOIN User n1 ON e0.dst=n1.id;`. 

Your task:
1. Navigate to `/app/libcypher2sql-0.5.0/` and fix the `Makefile`.
2. Locate the logic bug in `src/translator.cpp` that omits the join conditions and outputs a comma-separated `FROM` list instead of proper `JOIN` clauses for edges.
3. Compile the fixed program.
4. Copy the final working executable to `/home/user/cypher2sql`.

Our automated CI system will test `/home/user/cypher2sql` by passing it 500 randomly generated graph patterns and comparing its exact string output against a known-good, secure reference oracle.

Your fixed executable must run identically to the oracle. Do not change the CLI argument structure.