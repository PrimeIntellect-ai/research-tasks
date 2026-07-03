You are helping a computational biology researcher analyze a network dataset. 

A SQLite database is located at `/home/user/graph_data.db`. It contains the following schema:
- `nodes`: `(id INT, label TEXT, property TEXT)`
- `relations`: `(src INT, dst INT, type TEXT)`

The researcher needs to extract all instances of a specific graph motif: the **Feed-Forward Loop**. 
A feed-forward loop consists of three distinct nodes (A, B, C) connected by directed edges such that:
- A -> B (an edge exists from src A to dst B)
- B -> C (an edge exists from src B to dst C)
- A -> C (an edge exists from src A to dst C)

Additionally, the researcher only cares about motifs where **all three nodes** (A, B, and C) have their `property` column set to exactly `'target'`.

Your task is to:
1. Analyze the schema and create appropriate indexes on the `nodes` and `relations` tables to optimize the execution plan of this complex join. The database contains thousands of records, so it must be optimized.
2. Write a script (in Python, Bash, Ruby, or Perl) that executes the necessary SQL to find these motifs.
3. Output the result to `/home/user/motif_results.json`. The file should contain a JSON array of arrays, where each inner array represents one motif `[A_id, B_id, C_id]`.
4. The output list must be sorted lexicographically (first by `A_id`, then `B_id`, then `C_id`).

Make sure your results are accurately computed and saved to the exact path specified.