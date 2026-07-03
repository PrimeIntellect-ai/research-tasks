You are a database administrator tasked with optimizing queries for our production graph database. We've been experiencing severe performance degradation due to users submitting Cypher queries with unbounded or excessively deep recursive traversals (variable-length relationships).

You need to build a query sanitizer that filters out these dangerous queries.

**Part 1: Fix the Vendored Package**
We have a proprietary query parsing package vendored at `/app/vendored/cypher-validator-1.0`. It provides a useful function `extract_patterns(query_string)` that extracts the inner contents of all relationship brackets in a Cypher query (e.g., returning `["*1..3", ""]` for `MATCH (a)-[*1..3]->(b)-[]->(c)`). 
However, a junior developer recently broke the package. It currently fails to install and run. 
1. Fix the deliberate perturbations in the package (check the build config and imports).
2. Install the package in your environment.

**Part 2: Write the Sanitizer**
Create an executable script at `/home/user/sanitize.py`. 
Your script must accept a single command-line argument: a path to a directory containing `.cypher` files.
For each `.cypher` file in the directory, your script must read the query, use `cypher_validator.core.extract_patterns` to get the relationship patterns, and classify the query.

**Classification Rules:**
You must **REJECT** any query that contains a relationship pattern where the maximum traversal depth is strictly greater than 5, or is unbounded.
- Examples of REJECT: `*` (unbounded), `*..` (unbounded), `*1..` (unbounded), `*1..6` (max is 6 > 5), `*..10` (max is 10 > 5), `*7` (exact depth 7 > 5).
- Examples of ACCEPT: `*1..5` (max is 5), `*..4` (max is 4), `*3` (exact depth 3), or empty like ` ` or `:` (standard single-hop relationship).

**Output Format:**
For each file in the directory, print exactly one line to `stdout` in this format:
`<filename>: ACCEPT`
OR
`<filename>: REJECT`

Ensure your script works perfectly for both safe and adversarial queries.