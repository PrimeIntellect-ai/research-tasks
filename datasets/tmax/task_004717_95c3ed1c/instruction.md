I am a researcher organizing a dataset of academic papers, and I need help analyzing "citation deadlocks" (cyclic citations where papers form a closed loop of citations, often due to concurrent preprints). 

I have two datasets:
1. Relational metadata: `/home/user/data/metadata.csv` 
   Format: `paper_id,year,impact_score`
2. Graph edges: `/home/user/data/citations.txt`
   Format: `source_id,target_id` (representing a directed citation from source to target)

Please create a Rust project in `/home/user/analyzer` that reads these two files and processes them to find all isolated citation cycles. 

Your Rust program must:
1. Traverse the citation graph to identify all simple cycles (you can assume for this dataset that cycles are disjoint; no paper belongs to more than one cycle).
2. For each cycle, cross-reference the `metadata.csv` to find the `impact_score` of each paper in the cycle.
3. Compute an analytical aggregate: the maximum `impact_score` among all papers in that specific cycle.
4. Output the results to a JSON file at `/home/user/output/cycles_report.json`.

The output JSON must be an array of objects, with each object representing a cycle. 
Format requirements for `/home/user/output/cycles_report.json`:
- Each object must have a `"cycle"` key (an array of strings representing the `paper_id`s in the cycle, sorted lexicographically).
- Each object must have a `"max_score"` key (an integer representing the highest impact score in that cycle).
- The top-level JSON array must be sorted descending by `max_score`. If there's a tie, sort ascending by the first `paper_id` in the `"cycle"` array.

You can use standard Rust crates like `serde` and `serde_json` by configuring your `Cargo.toml`. Ensure your program runs successfully and generates the correct output file.