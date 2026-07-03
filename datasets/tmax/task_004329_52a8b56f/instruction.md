You are a data engineer building the final stage of an ETL pipeline that extracts hierarchical organizational data and computes employee influence (PageRank) across the corporate network.

There are three main parts to this task:

1. **Fix the Vendored Graph Library**: 
   We rely on a custom, third-party C++ graph processing package called `libfastgraph-1.2.0`, whose source is located at `/app/libfastgraph-1.2.0`. Recently, our build pipeline broke its performance due to a configuration perturbation introduced in its `Makefile` and `include/fastgraph_config.h`. 
   - Identify and fix the issues in the vendored package so it compiles correctly and efficiently. 
   - Build and install it locally in `/home/user/local/` (ensure headers go to `include/` and libraries to `lib/`).

2. **Extract Hierarchical Data**:
   There is an SQLite database at `/home/user/corporate.db`. It contains a table `personnel` (id, name, manager_id, department) and `interactions` (source_id, target_id, interaction_weight).
   - Write a C++ program `/home/user/pipeline.cpp` that connects to this SQLite database.
   - Use a **recursive CTE** to build an edge list of all indirect and direct management reporting lines (i.e., every employee has a directed edge to their manager, and their manager's manager, up the chain, with weight decreasing by a factor of 0.5 per hop).
   - Combine this hierarchal edge list with the `interactions` table using complex joins to produce a final unified directed edge list.

3. **Compute Graph Analytics**:
   - Using the `libfastgraph` library you compiled, ingest the extracted edge list.
   - Compute the PageRank centrality for every node in the unified graph.
   - Output the results to a CSV file at `/home/user/pagerank_results.csv` with the headers `id,pagerank`.

**Performance & Format Requirements**:
- Your pipeline must be highly optimized. The automated verifier will measure the end-to-end execution time of your compiled `pipeline` executable.
- The execution time must be under 1.5 seconds. (If you fail to fix the performance perturbation in `libfastgraph` or write poorly optimized SQL/C++, it will take much longer).
- The PageRank results must be numerically accurate.
- Compile your program as `/home/user/pipeline_exec`.

Make sure to leave `/home/user/pagerank_results.csv` properly formatted for the automated test suite.