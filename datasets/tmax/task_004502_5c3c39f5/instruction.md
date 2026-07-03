You are a data analyst responsible for auditing and optimizing graph database interactions before migrating to a new production Neo4j cluster. We have a large batch of legacy Cypher queries that need to be filtered to ensure they do not cause performance bottlenecks or violate pagination standards.

Your task is to write a Python script that acts as a query validator to automatically filter out unoptimized or dangerous queries.

1. First, inspect the image located at `/app/optimization_rules.png`. This image contains a slide with three crucial query optimization rules established by our Database Administrator regarding variable-length/recursive paths, result sorting, and pagination limits.
2. Write a Python script at `/home/user/query_validator.py`.
3. The script must accept exactly one command-line argument: the path to a text file containing a single Cypher query.
   Usage: `python3 /home/user/query_validator.py <path_to_query_file>`
4. The script must read the query and determine if it complies with **all** the rules found in the image.
5. If the query strictly complies with all rules, print exactly `VALID` to standard output and exit with status code `0`.
6. If the query violates *any* of the rules, print exactly `INVALID` to standard output and exit with status code `1`.

Note: You may use Python's built-in `re` module to parse the queries. You do not need to build a complete Cypher AST parser, as the test queries will be formatted reasonably consistently, but your regexes should be robust enough to handle varying whitespace, case-insensitivity for Cypher keywords (like `LIMIT`, `ORDER BY`), and different variable-length path syntax formats (e.g., `[*..3]`, `[*1..5]`).