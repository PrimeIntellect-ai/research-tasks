You are an ETL data engineer responsible for optimizing a knowledge graph pipeline. 

A legacy application uses a stripped, proprietary binary located at `/app/motif_oracle` to identify critical business entity patterns from graph data. The binary reads a tab-separated file of directed edges and outputs a sorted list of matched node IDs to `stdout`. 

Currently, the binary's runtime scales terribly. Your task is to reverse-engineer the graph pattern the oracle is matching and reimplement it in a highly optimized Python script.

**Inputs provided:**
1. `/home/user/sample_edges.tsv`: A small graph dataset (columns: `src`, `dst`, `type`, `weight`) you can use to test the oracle.
2. `/app/motif_oracle`: The stripped legacy binary. It is executed as `/app/motif_oracle <path_to_tsv>`.

**Requirements:**
1. Analyze the schema and deduce the subgraph pattern the oracle extracts.
2. Write a Python script at `/home/user/fast_motif.py`.
3. Your script must accept a single command-line argument (the path to a TSV file), execute the pattern matching, and print the resulting node IDs to `stdout` (one per line, sorted ascending), matching the exact format of the oracle.
4. Your implementation must perform query-to-pipeline chaining efficiently to handle large datasets. 

**Evaluation:**
The automated verifier will test `/home/user/fast_motif.py` against a hidden dataset (`/home/user/eval_edges.tsv`). To pass, your script must achieve a perfect F1 score against the oracle's output and execute at least 50x faster than the oracle on the evaluation set.