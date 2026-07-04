You are a data engineer building a secure ETL pipeline. We need a query validation tool to prevent malicious or unauthorized SQL queries from being executed against our data warehouse.

Your task is to build a Python CLI script at `/home/user/query_filter.py` that acts as a query sanitizer and access control filter. 

Requirements:
1. The script must take a single command-line argument: the path to a file containing a SQL query.
2. The script must output exactly `ACCEPT` to standard output if the query is safe, or `REJECT` if the query violates any security rules.
3. You must use the SQL parsing library `sqlglot` to analyze the queries. A vendored version of `sqlglot` (version 20.0.0) has been provided at `/app/vendor/sqlglot`. 
4. Note: Our CI pipeline reported that the vendored `sqlglot` package is currently broken due to a recent bad commit by a junior developer. You will need to find and fix the deliberate perturbation in the package before you can use it.
5. Security Rules for Queries:
   - Must ONLY be `SELECT` statements (including those with Common Table Expressions / `WITH` clauses). Any `INSERT`, `UPDATE`, `DELETE`, `DROP`, `ALTER`, etc., must be REJECTED.
   - Must NEVER read from the highly sensitive tables: `employee_salaries` or `system_credentials`. This applies even if the tables are aliased, hidden inside complex recursive CTEs, or nested within subqueries.

Testing:
You have been provided with two directories containing test cases:
- `/app/corpus/clean/`: Contains valid, complex queries (including hierarchical CTEs, pagination, and joins) that MUST be accepted.
- `/app/corpus/evil/`: Contains adversarial queries that attempt to bypass the rules using aliases, obfuscation, or unauthorized operations, which MUST be rejected.

Make sure your script works perfectly against both corpora.