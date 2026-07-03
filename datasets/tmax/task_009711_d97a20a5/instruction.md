You are a data engineer building an ETL pipeline to analyze a package dependency graph. 

You have been provided with an SQLite database at `/home/user/etl_data.db` (which you will need to assume exists with the schema described below).

The database contains a Directed Acyclic Graph (DAG) representing packages and their dependencies:
1. `nodes` table: `id` (INTEGER PRIMARY KEY), `name` (TEXT)
2. `edges` table: `source` (INTEGER), `target` (INTEGER)
   * A row `(A, B)` means package `A` depends on package `B`. 

**Your Objective:**
Write a C++ program at `/home/user/process_graph.cpp` that performs the following pipeline steps:
1. **Data Ingestion:** Read the graph from the SQLite database.
2. **Graph Analytics (Centrality/Hierarchical Impact):** Calculate the "Downstream Impact" score for *every* node. 
   * The "Downstream Impact" of node X is defined as the total number of *unique* nodes that depend on X directly or indirectly, plus 1 (for node X itself). 
   * In graph terms, this is the number of unique ancestors that can reach node X, plus 1.
3. **Sorting & Filtering:** Sort all nodes based on their Downstream Impact score in **descending** order. If there is a tie, sort by the node `id` in **ascending** order.
4. **Pagination:** Extract exactly Page 2 of the sorted results, where the page size is `4` items per page. (Assume 1-indexed pages, so Page 1 has items 1-4, Page 2 has items 5-8, etc.)
5. **Output:** Write this specific page of results to `/home/user/impact_page_2.csv`. The CSV must have the exact header `id,name,impact_score` and be comma-separated.

**Requirements:**
* You must implement the solution in C++17 or later.
* You may use shell commands to install dependencies (e.g., SQLite C++ libraries) and compile your code.
* Ensure your C++ program creates the output file `/home/user/impact_page_2.csv` upon execution.