You are a data engineer tasked with building a robust, reproducible ETL pipeline and similarity recommendation system in C.

Currently, user feature vectors are exported daily to `/home/user/input/features.csv`. The schema of this CSV is expected to be:
`id,f1,f2,f3,f4,f5`
Where `id` is a 32-bit integer, and `f1` through `f5` are double-precision floating-point numbers.

However, upstream data quality issues occasionally introduce anomalies:
- Missing numerical values are exported as the literal string `NaN`.
- Some rows have completely malformed `id` fields (e.g., strings like "invalid" or missing IDs).

Your task is to write a C program and an orchestrating Bash script to process this data, enforce the schema, and generate user recommendations based on feature similarity.

Step 1: Write a C program at `/home/user/pipeline.c` that does the following:
1. Opens and reads `/home/user/input/features.csv`. The first row is always the header.
2. Enforces the schema:
   - If the `id` field cannot be parsed as a valid integer, silently skip the entire row.
   - If any feature column (`f1` to `f5`) contains the string `NaN`, impute it with `0.0`.
3. Performs a Similarity Search / Recommendation:
   - For every valid user, find their "nearest neighbor" among all other valid users based on the Euclidean distance of their 5-dimensional feature vectors.
   - A user cannot be their own nearest neighbor.
   - If there is a tie in Euclidean distance, break the tie by choosing the neighbor with the **smaller** `id`.
4. Writes the results to `/home/user/output/recommendations.csv`.
   - The output must include a header: `id,nearest_neighbor_id`
   - The output rows must be sorted by `id` in ascending order.
   - Format both fields as integers.

Step 2: Create a reproducible pipeline script at `/home/user/run.sh` that:
1. Creates the `/home/user/output` directory if it doesn't exist.
2. Compiles `/home/user/pipeline.c` using `gcc` into an executable named `pipeline` in the home directory. You must link any necessary numerical/math libraries.
3. Executes the compiled `pipeline`.
4. To test pipeline reproducibility, your script must then rename `recommendations.csv` to `run1.csv`, execute the `pipeline` a second time, and save the second run as `run2.csv`.
5. Run `sha256sum` on `run1.csv` and write the checksum (just the standard output of sha256sum) to `/home/user/output/checksum.txt`.
6. Finally, move `run1.csv` back to `/home/user/output/recommendations.csv` and delete `run2.csv`.

Ensure your C code handles standard CSV reading gracefully and does not hardcode the number of rows (it should handle up to 10,000 users).

To complete the task, your script `/home/user/run.sh` must be executed successfully, leaving the expected outputs in `/home/user/output/`.