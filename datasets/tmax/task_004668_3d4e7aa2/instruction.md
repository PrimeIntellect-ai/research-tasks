You are a database administrator tasked with optimizing a highly inefficient knowledge graph query pipeline. 

Your company uses a proprietary, custom-built graph querying engine located at `/app/pattern_matcher`. This engine is provided as a stripped binary. It takes two arguments: a graph dataset file and a query file.

We have a large dataset located at `/home/user/raw_graph.tsv` containing millions of edges in the format:
`SourceNode \t RelationType \t TargetNode`

Our analytical team frequently runs a complex multi-hop pattern matching query, defined in `/home/user/slow_query.txt`. Currently, the engine takes an unacceptably long time to evaluate this query because it performs naive nested-loop joins for multi-hop patterns.

Your objectives:
1. Analyze `/app/pattern_matcher` to understand its expected input formats and how it parses queries (you can run it against small dummy files to observe its behavior).
2. Write a Python script at `/home/user/optimize_pipeline.py` that reads `/home/user/raw_graph.tsv` and performs **graph materialization/projection**. It should pre-compute the heavy multi-hop patterns and output a new, optimized graph file at `/home/user/projected_graph.tsv`.
3. Create a rewritten, logically equivalent query file at `/home/user/fast_query.txt` that utilizes your newly materialized edges to bypass the expensive joins.
4. Ensure that running `/app/pattern_matcher /home/user/projected_graph.tsv /home/user/fast_query.txt` yields the exact same logical result count as the original, but runs significantly faster.

You must leave your final optimized graph at `/home/user/projected_graph.tsv` and the updated query at `/home/user/fast_query.txt`. Your pipeline will be tested for equivalence and performance.