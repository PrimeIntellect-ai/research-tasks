You are an MLOps engineer tasked with fixing an experiment tracking pipeline. 

There is a C program located at `/home/user/normalize_and_bootstrap.c` that processes a dataset (`/home/user/data.csv`). The script:
1. Parses the CSV dataset (enforcing a specific 3-column schema: id, value, split).
2. Calculates the mean and standard deviation of the `value` column to normalize the data.
3. Outputs the mean of the normalized "test" split to `/home/user/test_mean.txt`.
4. Performs 1000 bootstrap samples on the normalized "train" split to estimate its mean, outputting the result to `/home/user/bootstrap_mean.txt`.

However, the current implementation has a severe **data leakage** bug. The scaling statistics (mean and standard deviation) are computed using the *entire* dataset, mixing "train" and "test" records. 

Your task:
1. Inspect and modify `/home/user/normalize_and_bootstrap.c` to fix the data leakage.
2. The mean and standard deviation used for normalization must be computed **ONLY** from the records where `split` is `"train"`.
3. Normalize both the "train" and "test" records using the isolated "train" statistics.
4. Do not alter the random seed, the number of bootstrap iterations, or the output file paths/formats.
5. Compile the C program (e.g., `gcc normalize_and_bootstrap.c -lm -o run_pipeline`) and execute it. 
6. Ensure the corrected `/home/user/test_mean.txt` and `/home/user/bootstrap_mean.txt` are generated.