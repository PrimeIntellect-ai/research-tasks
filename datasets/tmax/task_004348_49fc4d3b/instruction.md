You are an AI assistant helping a data scientist clean a dataset of feature embeddings. The dataset is located at `/home/user/data/embeddings.csv`. It contains 50 rows and 10 columns of floating-point numbers representing high-dimensional embeddings.

Your task is to implement a robust data cleaning pipeline in **C** that removes highly correlated features (a form of dimensionality reduction), and then wrap it in a bash script to test pipeline reproducibility.

Here are your instructions:

1. **Write a C program** at `/home/user/cleaner.c`:
   - It should read `/home/user/data/embeddings.csv` (comma-separated, no header).
   - It must compute the Pearson correlation coefficient between all pairs of columns (features).
   - Identify redundant columns: Iterate through the columns from index 0 to 9. For each column $i$, check all subsequent columns $j$ (where $j > i$). If the absolute Pearson correlation between column $i$ and column $j$ is strictly greater than `0.85`, mark column $j$ to be dropped (if it hasn't been marked already).
   - Write the cleaned dataset (retaining only the columns that were not dropped) to `/home/user/clean_embeddings.csv`. The output should be comma-separated, with each float printed to exactly 6 decimal places (e.g., using `%.6f`).

2. **Write a reproducibility test script** at `/home/user/test_pipeline.sh`:
   - The script must compile `cleaner.c` into an executable named `cleaner` (make sure to link the math library using `-lm`).
   - Run the executable on the provided dataset to produce `/home/user/clean_embeddings.csv`.
   - Run the executable a second time to produce `/home/user/clean_embeddings_run2.csv`.
   - Compute the MD5 checksums of both output files and compare them.
   - If the files are identical (reproducible), the script should print "PASS: Reproducible" and exit with code 0.
   - If they differ, print "FAIL: Non-deterministic" and exit with code 1.

3. **Execution**: Make sure `test_pipeline.sh` is executable (`chmod +x`).

Notes:
- You may use standard C libraries (`stdio.h`, `stdlib.h`, `math.h`, `string.h`). No external linear algebra libraries are required or provided.
- You must create the `/home/user/cleaner.c` and `/home/user/test_pipeline.sh` files.
- Ensure the output CSV has no trailing commas on each line.