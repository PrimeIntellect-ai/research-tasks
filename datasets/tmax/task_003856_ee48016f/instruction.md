You are a database administrator tasked with optimizing and securing our query pipeline. 

We have a custom SQL query builder package vendored at `/app/vendored_sql_builder`. This package is used to generate complex hierarchical and aggregation queries. However, a recent update introduced a bug that causes it to generate invalid syntax when compiling recursive Common Table Expressions (CTEs).
Your first task is to locate and fix the bug in the vendored package.

Once the query builder is fixed, you need to implement a query sanitizer. We have noticed that some generated queries result in catastrophic execution plans due to missing join conditions (Cartesian explosions) or unbounded recursive CTEs. 
Write a Python script at `/home/user/query_sanitizer.py` that analyzes a given SQL file and determines whether it is "safe" or "unsafe".
The script should be executable and accept a single file path as an argument.
It must exit with code 0 if the query is safe, and exit with code 1 if the query is unsafe.

A query is considered unsafe (evil) if:
1. It contains a recursive CTE but lacks a termination condition (e.g., no `LIMIT` or missing `WHERE` clause in the recursive step).
2. It performs cross-query aggregation resulting in an explicit `CROSS JOIN` without a `WHERE` filter applied to the joined tables.

A query is safe (clean) if it properly bounds recursive CTEs and uses `INNER JOIN` or filters cross joins.

To test your sanitizer, we have provided two directories containing generated SQL queries:
- `/home/user/corpora/clean/`: Contains well-formed, optimized queries.
- `/home/user/corpora/evil/`: Contains queries that will cause performance issues.

Your script must correctly accept 100% of the queries in the clean corpus and reject 100% of the queries in the evil corpus.