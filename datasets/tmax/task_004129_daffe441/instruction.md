You are helping a researcher organize large citation datasets using an automated query pipeline. The researcher relies on a vendored Python package to materialize graph projections and complex joins.

However, there are two major issues:
1. The vendored package `sql-graph-proj` (located at `/app/sql-graph-proj-1.0.0`) is currently broken and cannot be installed due to a bad dependency in its configuration, and it has a hardcoded bug in its SQL generation logic that produces Cartesian products instead of proper joins.
2. The researcher receives raw SQL queries from external students. Some queries accidentally contain implicit cross joins (e.g., `FROM authors, papers` with no `WHERE` clause), which crash the database due to memory exhaustion. 

Your tasks:
1. **Fix the Vendored Package**: 
   - Locate `/app/sql-graph-proj-1.0.0`. 
   - Fix the `setup.py` so it can be installed via `pip install -e .`.
   - Fix the internal bug in the package's `compiler.py` where it hardcodes `"CROSS JOIN"` instead of the intended `"INNER JOIN"`.

2. **Create an Adversarial SQL Filter**:
   - Write an executable script at `/home/user/sql_filter.py`.
   - The script must take a single command-line argument: the path to a `.sql` file.
   - It must analyze the query and **exit with code 0** (accept) if the query is a safe, explicit join (e.g., contains `INNER JOIN` or `JOIN ... ON`).
   - It must **exit with code 1** (reject) if the query contains an implicit cross join (e.g., a comma-separated `FROM a, b` without any `WHERE` clause) or an explicit `CROSS JOIN`.
   - You must ensure your script correctly classifies the queries in the researcher's corpora:
     - `/app/corpus/clean/` (contains only valid join queries)
     - `/app/corpus/evil/` (contains queries that produce Cartesian explosions)

Your final filter must achieve a 100% pass rate on both the clean and evil corpora.