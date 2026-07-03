You are a Machine Learning Engineer preparing a simplified training data pipeline. We need to parse a raw dataset, compute heuristic "embeddings" (feature vectors) for text, and perform a retrieval task to find the closest matches for a set of queries.

You must write a C++ program to perform the heavy lifting and a bash script to create a reproducible pipeline.

**Step 1: Data Schema Enforcement**
You will be provided with `/home/user/raw_data.tsv`. The file has no header. Each line is separated by tabs and should contain exactly three columns: `ID`, `Category`, and `Text`.
A row is only valid if:
1. `ID` is a strictly positive integer.
2. `Category` is a non-empty string containing only alphabetic characters.
3. `Text` is a non-empty string with at least 5 characters.
If a row is invalid, its 1-based line number should be appended to `/home/user/invalid_rows.log` (one integer per line).

**Step 2: Embedding Computation**
For each valid row, compute a 5-dimensional feature vector based on the `Text` column:
- Dimension 0: The length of the text string.
- Dimension 1: The number of vowels (A, E, I, O, U, a, e, i, o, u).
- Dimension 2: The number of consonants (alphabetic characters that are not vowels).
- Dimension 3: The number of uppercase letters (A-Z).
- Dimension 4: The number of space characters (' ').
Normalize this 5-dimensional vector to unit length (L2 norm = 1.0). If the vector has an L2 norm of 0 (e.g., empty or invalid text, though schema enforces >4 chars), ignore the row and treat it as invalid.
Output the valid vectors to `/home/user/valid_embeddings.csv` in the format:
`ID,v0,v1,v2,v3,v4` (vectors formatted to 4 decimal places).

**Step 3: Retrieval**
You will be provided with a query dataset `/home/user/queries.tsv` with the same format as `raw_data.tsv`.
Apply the same schema enforcement and embedding computation to the queries.
For each valid query, find the single most similar embedding from `valid_embeddings.csv` using Cosine Similarity. If there is a tie, pick the one with the lowest `ID`.
Output the results to `/home/user/retrieval_results.csv` in the format:
`Query_ID,Matched_ID,Cosine_Similarity` (Cosine similarity rounded to 4 decimal places).

**Step 4: Pipeline Construction**
Create a reproducible bash script at `/home/user/run_pipeline.sh` that:
1. Compiles your C++ code (e.g., `pipeline.cpp`) using `g++` with `-std=c++17` and `-O3`.
2. Runs the executable against `/home/user/raw_data.tsv` and `/home/user/queries.tsv`.
3. Ensures all output files (`invalid_rows.log`, `valid_embeddings.csv`, `retrieval_results.csv`) are generated in `/home/user/`.

**Constraints:**
- Do not use any external C++ libraries outside the standard library.
- Make sure `run_pipeline.sh` is executable (`chmod +x`).