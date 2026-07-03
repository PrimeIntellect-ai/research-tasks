You are a data engineer migrating a legacy knowledge graph ETL pipeline to a modern Python-based stack. 

The previous pipeline relies on a proprietary, compiled C++ binary located at `/app/legacy_matcher` to perform graph pattern matching, cross-query aggregation, and path evaluation. We have lost the source code for this binary. 

Your objective is to write a replacement Python script at `/home/user/new_matcher.py` that behaves EXACTLY like the legacy binary. It must read from `stdin` and print to `stdout` with identical formatting and logic.

We know the input format of the binary:
1. The first line contains three integers separated by spaces: `N M Q`
   - `N`: Number of nodes (nodes are implicitly labeled `0` to `N-1`)
   - `M`: Number of directed edges
   - `Q`: Number of path queries
2. The next `M` lines define the edges, each containing: `u v weight type`
   - `u`, `v`: Integers representing the source and destination nodes (the graph is guaranteed to be a Directed Acyclic Graph).
   - `weight`: A floating-point number.
   - `type`: A string representing the edge relationship (e.g., `HAS_A`, `KNOWS`).
3. The next `Q` lines define the queries, each containing: `start end sequence`
   - `start`, `end`: Integers representing the start and target nodes.
   - `sequence`: A comma-separated list of edge types representing the exact path schema that must be matched (e.g., `HAS_A,KNOWS,HAS_A`).

Output:
The binary outputs exactly `Q` lines. Each line corresponds to a query and contains a single floating-point number formatted to exactly 4 decimal places.

Your task:
1. Analyze the binary `/app/legacy_matcher` by passing it various test inputs.
2. Deduce the exact mathematical aggregation and pattern matching logic it uses to evaluate these typed paths.
3. Implement the equivalent logic in `/home/user/new_matcher.py`. 

The automated test will generate hundreds of random DAGs and schemas, feed them to both the legacy binary and your Python script, and assert that the outputs are bit-for-bit identical. Ensure edge cases (like no valid paths) are handled exactly as the binary handles them.