You are an AI assistant helping a researcher organize their dataset of academic papers and citation networks.

The researcher has a SQLite database located at `/home/user/research.db`. It contains two tables:
1. `papers`: `id` (INTEGER PRIMARY KEY), `title` (TEXT), `year` (INTEGER), `score` (REAL)
2. `citations`: `source_id` (INTEGER), `target_id` (INTEGER) representing a directed citation from source to target.

Your task is to write and execute a Rust program that analyzes this database. 

Create a new Cargo project at `/home/user/citation_processor`. You may use `rusqlite` and `serde_json` (and any other standard ecosystem crates like `serde`) in your `Cargo.toml`.

Your Rust program must perform the following logical steps:
1. **Graph Traversal:** Find the shortest citation path from the paper with `id = 1` to the paper with `id = 5`. (If there are multiple paths of the same shortest length, pick any).
2. **Analytical Aggregation (Windowing):** For all papers in the database, calculate their "year rank". The year rank is the `DENSE_RANK` of the paper within its publication `year`, ordered by `score` descending. (The highest score in a given year has rank 1).
3. **Filtering & Sorting:** Filter the results to ONLY include the papers that are part of the shortest path found in Step 1. Order the final results in the exact sequence of the citation path (from the starting paper `id = 1` down to the target paper `id = 5`).
4. **Format Conversion & Export:** Export the resulting data as a JSON array to `/home/user/path_results.json`. Each element in the JSON array must be an object with the following keys and correct types:
   - `id` (integer)
   - `title` (string)
   - `year` (integer)
   - `score` (float)
   - `year_rank` (integer)

Ensure you build and run your Rust program so that `/home/user/path_results.json` is generated correctly. Do not alter the database.