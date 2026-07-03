You are a Database Administrator managing a high-performance graph database. We allow data scientists to submit Cypher queries for complex graph analytics (like centrality and clustering algorithms), but we recently experienced severe database degradation due to poorly optimized and malicious queries (e.g., unbounded variable-length paths, Cartesian products, and unauthorized mutating queries like `DETACH DELETE`).

We need to implement a robust Cypher query sanitizer. 

**Part 1: Fix the Vendored Package**
We vendor a Python-based Cypher parsing library at `/app/vendored/cypher-parser` to parse and lint queries without hitting the database. However, the build is currently broken due to a deliberate perturbation in its `Makefile` (it is missing the `-std=c++11` compiler flag required for compilation on our current OS). 
1. Diagnose and fix the build process in `/app/vendored/cypher-parser`.
2. Compile and install it so it can be imported in Python as `cypher_parser`.

**Part 2: Build the Adversarial Query Filter**
Write a script at `/home/user/query_filter.py` that acts as a query sanitizer. Your script must process a directory of `.cypher` files.
It should classify each query as either `ACCEPT` or `REJECT`.
You must REJECT queries that contain:
- Mutating operations (`CREATE`, `MERGE`, `SET`, `DELETE`, `REMOVE`, `DROP`).
- Unbounded variable-length paths (e.g., `[*]` or `[*..]`).
- Cartesian products (multiple disconnected `MATCH` patterns without a relationship or explicit `WHERE` join condition).
You must ACCEPT clean queries performing safe operations (e.g., standard aggregations, bounded PageRank/centrality projections).

Your script must take an input directory and an output log file as arguments:
`python3 /home/user/query_filter.py --input-dir <dir> --output-log <file>`

The output log must contain one line per file processed, formatted exactly as:
`<filename>: <ACCEPT|REJECT>`

**Part 3: Testing**
Test your script against the provided corpora:
- `/app/corpora/evil/`: Contains queries designed to exhaust resources or mutate data.
- `/app/corpora/clean/`: Contains valid graph analytic queries.

Ensure your script correctly categorizes 100% of the files in both directories. Leave the final output of your runs in `/home/user/evil_results.log` and `/home/user/clean_results.log`.