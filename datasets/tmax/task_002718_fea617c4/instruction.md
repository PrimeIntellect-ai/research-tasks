We are using a lightweight, command-line graph database engine called `tiny-graph-db` to perform fast graph analytics and traverse our network topology data. As a Database Administrator, your task is to fix our locally vendored build of this tool, and then write a Bash script to sanitize incoming graph query requests to prevent Denial of Service (DoS) attacks caused by overly complex traversals.

Part 1: Fix the Vendored Package
The source code for `tiny-graph-db` (version 1.2.0) is vendored at `/app/tiny-graph-db`. Currently, it fails to compile because of a deliberate or accidental perturbation in its `Makefile` (an incorrectly set compiler flag that breaks the build on our architecture).
1. Identify and fix the build issue in `/app/tiny-graph-db/Makefile`.
2. Compile the package and ensure the `tiny-graph-db` executable is successfully built in `/app/tiny-graph-db/bin/`.

Part 2: Build the Query Sanitizer
Users submit graph queries in a custom syntax. Some queries are malicious and specify unbounded traversals (e.g., `MATCH (a)-[*]->(b)`) or extremely deep bounded traversals (e.g., `MATCH (a)-[*1..100]->(b)`), which bring the system to a halt.
Write a Bash script at `/home/user/query_sanitizer.sh` that takes a single query string as an argument.
- It must output `ACCEPT` and exit with code 0 if the query is safe.
- It must output `REJECT` and exit with code 1 if the query is unsafe.

A query is considered UNSAFE (evil) if it contains:
1. Unbounded variable-length paths: `[*]` or `[*..]` or `[*..N]` where the lower bound is omitted or `[*M..]` where the upper bound is omitted.
2. Bounded variable-length paths where the maximum depth is greater than 5 (e.g., `[*1..6]`, `[*2..10]`).

A query is SAFE (clean) if it contains:
1. No variable-length paths (e.g., `MATCH (a)->(b)`).
2. Bounded variable-length paths where the maximum depth is 5 or less (e.g., `[*1..5]`, `[*2..3]`).

Make sure your script is executable (`chmod +x /home/user/query_sanitizer.sh`).