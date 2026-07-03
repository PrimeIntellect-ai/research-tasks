You are an expert Database Administrator managing a graph-processing backend powered by SQLite. We have a legacy system where an upstream service generates complex SQL queries to traverse a graph of relationships (stored as an edge list). 

Recently, we discovered that one of our critical tables has a corrupted index. Certain maliciously crafted complex joins and subqueries are forcing SQLite to return stale or corrupted rows by coercing the query planner to use the broken index. We cannot rebuild the index right now due to an ongoing migration lock.

We have a proprietary query generator tool located at `/app/query_gen` (a stripped binary). We don't have its source code, but we know it outputs graph-traversal SQL queries. 

Your task is to write a Python CLI script at `/home/user/sanitizer.py` that acts as a query firewall. 
1. The script must accept a single SQL query via standard input.
2. It must analyze the query's joins, subqueries, and table references.
3. It must print the exact original query to standard output if the query is safe ("clean").
4. If the query attempts to exploit the corrupted index pattern, it must output "REJECTED" and exit with code 1.

You have been provided with two directories containing sample SQL queries:
- `/home/user/corpus/clean/`: Contains 50 safe graph-traversal queries. Your script MUST preserve and output these exactly as they are.
- `/home/user/corpus/evil/`: Contains 50 queries known to trigger the corrupted index behavior. Your script MUST reject all of these.

To succeed, you must reverse-engineer the logic used by `/app/query_gen` to understand the graph querying schema, analyze the differences between the clean and evil queries, and write a robust Python script that correctly validates the query schema and structure. You can use standard Python libraries.

Your final output will be evaluated against a hidden test suite using the same criteria. You must achieve a 100% rejection rate for the evil corpus and a 100% pass rate for the clean corpus.