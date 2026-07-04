You are an MLOps engineer tasked with building a lightweight artifact processing pipeline using only standard Linux CLI tools. 

We have a set of experimental embeddings saved in a CSV file. We need to perform feature engineering, dimensionality reduction, and linear algebra operations to evaluate the magnitude of our experiment vectors after dropping the least informative feature.

Your task is to write a Bash script at `/home/user/process.sh` that does the following:

1. Reads the raw embeddings from `/home/user/artifacts/embeddings.csv`. The file has a header `id,f1,f2,f3` followed by 4 rows of data.
2. Performs feature engineering by **mean-centering** each feature (f1, f2, f3) across all rows (subtract the column mean from each value).
3. Evaluates the population variance for each mean-centered feature.
4. Performs dimensionality reduction (feature selection) by **dropping the 1 feature with the lowest variance**, keeping the 2 features with the highest variance.
5. Computes the **L2 norm** (Euclidean distance from the origin) of the resulting mean-centered 2D vector for each row.
6. Outputs the final results to `/home/user/processed_norms.csv`.

**Output Format:**
The output file `/home/user/processed_norms.csv` must contain a header `id,l2_norm`.
The `l2_norm` values must be rounded to exactly 2 decimal places.
Example:
```
id,l2_norm
exp1,3.20
```

You must ensure that `/home/user/process.sh` is executable and successfully generates `/home/user/processed_norms.csv` when run. Do not use Python; rely on standard Unix utilities like `bash`, `awk`, `bc`, or `sed`.

(Note: You will need to create the directory `/home/user/artifacts` and the file `/home/user/artifacts/embeddings.csv` yourself with the following data before running your script):
```
id,f1,f2,f3
exp1,2.0,2.0,1.0
exp2,6.0,8.0,1.1
exp3,3.0,5.0,0.9
exp4,5.0,3.0,1.2
```