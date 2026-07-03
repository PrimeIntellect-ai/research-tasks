You are acting as a database administrator for a data analytics company. We are modernizing our data infrastructure and need to deprecate a legacy, closed-source graph querying engine. 

The legacy engine is provided as a compiled Linux binary located at `/app/query_oracle`. We have lost the source code for this engine, and it has been stripped of debugging symbols. 

Your task is to write a Python script at `/home/user/graph_query.py` that behaves **exactly** like `/app/query_oracle`. It must be a drop-in replacement that reads from standard input and writes to standard output, matching the original binary's logic, output formatting, and edge-case handling bit-for-bit.

To accomplish this, you must:
1. Experiment with `/app/query_oracle` by feeding it standard input to deduce its accepted data format, the structure of its commands, and its expected output.
2. The legacy engine performs "query-to-pipeline chaining" for knowledge graph pattern matching. It reads a directed graph (edges with relationships) and then processes a series of queries that trace paths through the graph (essentially performing multiple complex joins).
3. Implement the exact same graph traversal and join logic in Python.
4. Ensure your script is optimized enough to handle graphs of up to 10,000 edges without timing out.

Write your final implementation to `/home/user/graph_query.py`. An automated fuzzing system will test your script against the legacy binary with thousands of random graphs and query chains to ensure bit-exact output equivalence.