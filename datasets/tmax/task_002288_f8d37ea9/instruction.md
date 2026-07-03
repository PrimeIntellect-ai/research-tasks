You are an AI assistant helping a data researcher analyze a knowledge graph of datasets. 

I have an SQLite database located at `/home/user/datasets.db` containing two tables representing a knowledge graph of datasets and their derivations:
1. `datasets (id INTEGER PRIMARY KEY, name TEXT, domain TEXT, size_mb INTEGER)`
2. `derivations (source_id INTEGER, target_id INTEGER, method TEXT)`

I need you to create a Rust project to analyze this graph. Please do the following:
1. Initialize a new Cargo binary project at `/home/user/graph_analyzer`.
2. Add the `rusqlite` crate (version "0.31.0", with the "bundled" feature).
3. Write a Rust program in `src/main.rs` that connects to `/home/user/datasets.db` and executes a single, advanced SQL query to:
   - Perform a **graph traversal** (using a Recursive CTE) to find all datasets that are downstream derivations (direct or indirect) starting from the dataset named `'Root_Alpha'`.
   - Calculate the shortest `path_length` (number of derivation edges) from `'Root_Alpha'` to each reachable dataset. `'Root_Alpha'` itself has a path length of 0.
   - Using a **window function**, calculate the `DENSE_RANK()` of each reachable dataset based on its `size_mb` (in DESCENDING order), partitioned by the dataset's `domain`.
   - Perform a **knowledge graph pattern match**: filter the final results to ONLY include datasets whose derivation path (from 'Root_Alpha') includes at least one edge where `method = 'filter'`. (Hint: You can track this as a boolean or string flag within your recursive CTE).
4. The Rust program must execute this query and write the results directly to a CSV file at `/home/user/derivation_report.csv`.
5. The CSV must have exactly this header: `name,domain,size_mb,path_length,domain_rank`. Sort the CSV rows alphabetically by `name`.

After writing the code, build and run your Rust program to generate the `/home/user/derivation_report.csv` file.