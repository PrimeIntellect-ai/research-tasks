You are acting as a data engineer assisting a data analyst in building a reproducible processing pipeline for embedding data. We have batches of CSV files containing pairs of embeddings, and we need a reliable Bash pipeline to compute their cosine similarity, perform threshold validation, and extract the relevant records. 

Unfortunately, our standard numerical utility package has a bug and fails to compile, so you must fix it first before writing the pipeline.

**Step 1: Fix the Vendored Numerical Utility**
We use a lightweight C utility to compute embeddings fast. Its source is located at `/app/lib-embed-tools`. 
1. Navigate to `/app/lib-embed-tools`.
2. Inspect the `Makefile`. There is a configuration bug preventing the successful linking of the math library (which provides functions like `sqrt` used in `src/main.c`). 
3. Fix the `Makefile` and run `make`. This should successfully produce the executable `/app/lib-embed-tools/bin/cosine_sim`.
*(Note: The utility `cosine_sim` takes two colon-separated vectors as arguments and prints their cosine similarity as a float, e.g., `./cosine_sim 0.1:0.2 0.3:0.4`)*

**Step 2: Build the Data Pipeline**
Write a Bash script at `/home/user/pipeline.sh` that takes exactly one argument: the path to an input CSV file. 

The input CSV files will NOT contain a header. Each row will have exactly three comma-separated fields:
`id,embedding_A,embedding_B`
*   `id`: An alphanumeric string.
*   `embedding_A` and `embedding_B`: Colon-delimited floats of equal dimension (e.g., `0.23:-0.45:0.89`).

Your script `/home/user/pipeline.sh` must:
1. Iterate over every line in the provided CSV.
2. For each line, use the `/app/lib-embed-tools/bin/cosine_sim` tool to compute the similarity between `embedding_A` and `embedding_B`.
3. **Model output validation:** We only want to keep highly similar pairs. Filter the results such that you only output rows where the cosine similarity is **greater than or equal to 0.5000**. (You can use `bc` or `awk` for this float comparison).
4. For the rows that pass validation, print the result to standard output in the format: `id,similarity_score` (e.g., `row42,0.8521`).
5. Ensure your script prints nothing else to `stdout` except the passing rows in the exact order they appeared in the input file.

Ensure your script is executable (`chmod +x /home/user/pipeline.sh`). Automated test suites will verify your script against numerous randomly generated CSV files, asserting bit-exact equivalence with our reference pipeline.