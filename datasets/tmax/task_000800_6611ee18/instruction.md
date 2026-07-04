You are a database administrator tasked with optimizing and securing a proprietary knowledge graph database. The database uses a custom query execution engine, but recently, poorly optimized or malicious graph queries have been causing performance degradation, exponential traversal explosions, and Out-Of-Memory (OOM) errors.

To protect the system, you must create a pre-execution query sanitizer. You have been provided with:
1. A stripped, proprietary query planner binary located at `/app/query_engine`. This binary simulates the query execution plan. When run as `/app/query_engine <query_file.json>`, it exits with `0` if the query plan is safe and efficient, and exits with a non-zero code (or crashes) if the query is unsafe or poorly optimized.
2. A corpus of known safe, performant queries in `/app/corpus/clean/`.
3. A corpus of known dangerous, unoptimized queries in `/app/corpus/evil/`.

These queries are written in a custom JSON-based Graph DSL that specifies node pattern matching, cross-representation mapping (e.g., joining graph nodes to document stores), graph traversals, shortest path computations, and result pagination.

Your task is to write a Python script at `/home/user/sanitizer.py` that analyzes a given JSON query and statically determines if it is safe to run, *without* invoking the `/app/query_engine` binary (which is too slow for production pre-filtering).

Requirements for `/home/user/sanitizer.py`:
- Must be executable and accept exactly one positional argument: the path to a JSON query file.
- Must parse the JSON and analyze its filtering, pagination, graph traversal depth, and mapping properties.
- Must exit with status code `0` if the query is structurally safe (Clean).
- Must exit with status code `1` if the query violates the optimization/safety rules (Evil).
- Must process the file strictly in Python using standard libraries (do not use `subprocess` to call the binary).

You should use the provided binary and corpora to reverse-engineer the exact constraints and rules that determine whether a query is safe or evil. Think carefully about pagination limits, bounded traversals, and indexed cross-representation lookups.