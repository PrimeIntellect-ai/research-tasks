You are an AI assistant helping a researcher organize and analyze a large dataset of academic papers using an in-house graph processing library. 

The researcher has a NoSQL document dataset located at `/home/user/data/papers.jsonl`. Each line is a JSON object representing a paper, its authors, and its references.

We are using an in-house graph analysis tool currently vendored at `/app/vendored/py-graph-engine/`. 
However, the researcher noticed that querying and projecting the co-authorship graph using this library takes far too long, making iterative analysis impossible.

Your objectives are:

1. **Fix the Vendored Package**: 
   The `py-graph-engine` has a severe performance bottleneck. Inspect `/app/vendored/py-graph-engine/core/executor.py`. The `build_edge_list` function attempts to resolve node references using a naive nested loop structure that mimics a poorly optimized `O(N^2)` query plan. 
   Modify this function to use an optimal `O(N)` hash-based join strategy (using Python dictionaries) so that graph materialization scales efficiently.

2. **Graph Materialization & NoSQL Aggregation**:
   Write a Python script `/home/user/analyze.py` that imports `py-graph-engine` (make sure your script sets the `PYTHONPATH` or `sys.path` correctly). 
   Use the package to:
   - Ingest `/home/user/data/papers.jsonl`.
   - Filter out papers published before 2010.
   - Project a **Co-Authorship Graph**: Nodes are author names. An undirected edge exists between two authors if they co-authored at least one paper together (in the filtered dataset). Edge weights should equal the number of co-authored papers.

3. **Graph Analytics**:
   Compute the Degree Centrality (sum of edge weights connected to an author) for every author in the projected graph. 

4. **Output**:
   Save your final graph centrality metrics to `/home/user/centrality_results.json`.
   The file must be a JSON object mapping author names (strings) to their degree centrality (integers):
   ```json
   {
     "Alice Smith": 12,
     "Bob Jones": 8,
     ...
   }
   ```

**Performance & Accuracy Constraints:**
Your solution will be tested against a strict metric threshold. 
- The materialization and analytics script must achieve a **>= 20x speedup** compared to the unoptimized `O(N^2)` package on the hidden test dataset.
- The Mean Squared Error (MSE) of your centrality metrics compared to the ground truth must be **0.0** (exact match).