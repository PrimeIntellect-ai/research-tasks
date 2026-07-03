You are a researcher organizing a graph dataset of academic publications. You have been provided a JSON file containing a bipartite knowledge graph of authors and papers. You need to write a Go program to reverse-engineer the implicit co-authorship data model, extract specific graph patterns, and export the results to a structured CSV.

The dataset is located at `/home/user/dataset.json`.
It contains an object with two keys: `nodes` and `edges`.
- `nodes` have an `id` and a `type` (either "Author" or "Paper").
- `edges` have a `source` (an Author ID) and a `target` (a Paper ID), representing a "Wrote" relationship.

Your task is to:
1. Parse the JSON file and infer the implicit "Co-Author" graph. Two authors are considered co-authors if they both have an edge to the exact same Paper.
2. Find all distinct "triangles" of authors. A triangle is a group of exactly 3 authors where *every* pair within the group has co-authored at least one paper together.
3. For each triangle, calculate its "collaboration strength". This is the sum of the number of shared papers for all three author pairs in the triangle. (e.g., if A and B share 2 papers, B and C share 1 paper, and A and C share 1 paper, the strength is 4).
4. Export the results to `/home/user/triangles.csv`.

**Output Schema Requirements for `triangles.csv`:**
- The CSV must have exactly four columns with the header: `author1,author2,author3,strength`
- Each row represents one distinct triangle.
- For each row, the author IDs must be sorted alphabetically horizontally (i.e., `author1` < `author2` < `author3`).
- The rows in the CSV must be sorted descending by `strength`. If there is a tie in strength, sort ascending by `author1`, then `author2`, then `author3`.

Write and execute the Go code to produce this CSV.