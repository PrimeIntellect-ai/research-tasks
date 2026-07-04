You are a data scientist working on an embedded systems project where Python is not available. You need to preprocess a raw sensor dataset using C to handle missing values, engineer a new feature, and clamp outliers. You will also perform a simple hyperparameter search to find the optimal outlier threshold.

The dataset is located at `/home/user/raw_data.csv`. It has a header row and three columns: `id`, `val1`, and `val2`.

Perform the following steps:
1. Write a C program named `/home/user/preprocess.c` that accepts exactly two arguments: the input CSV file path and an integer threshold `T`.
2. The C program should read the CSV file line by line (skipping the header) and perform the following data cleaning and feature engineering:
   - **Missing Value Handling**: If `val1` or `val2` is `-999`, replace it with `0`.
   - **Feature Engineering**: Compute a new engineered feature `val3 = (val1 * val1) + val2`.
   - **Outlier Handling**: Clamp `val3` so that it does not exceed the threshold `T`. If `val3 > T`, set `val3 = T`.
3. The C program should compute the arithmetic mean of the final `val3` values across all rows and print ONLY this mean to standard output (as a float or double, up to at least 2 decimal places).
4. Write a bash script `/home/user/tune.sh` that:
   - Compiles `/home/user/preprocess.c` using `gcc`.
   - Performs a parameter sweep (tuning) over the following threshold `T` values: `10, 50, 100, 150, 200`.
   - Runs the compiled C program for each `T`.
   - Finds the **smallest** threshold `T` (from the list above) that results in a mean `val3` strictly greater than `50.0`.
   - Writes only that chosen integer threshold `T` into a file named `/home/user/best_t.txt`.

Ensure your bash script runs correctly and successfully produces the `/home/user/best_t.txt` file.