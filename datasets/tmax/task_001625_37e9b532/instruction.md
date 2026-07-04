You are an MLOps engineer analyzing tracking artifacts from a recent machine learning experiment. During the experiment, various pipeline configurations were tested, including a dimensionality reduction step using PCA with different numbers of components.

You have two space-separated text files:
1. `/home/user/experiments.txt`: Contains the experiment metadata with columns `id` and `pca_components`.
2. `/home/user/metrics.txt`: Contains the results with columns `id` and `accuracy`.

Your task is to:
1. Join these two files on the `id` column using standard Linux command-line tools. Note that both files have headers.
2. Filter the joined data to keep only the experiments where `pca_components` is exactly `10`.
3. Write a C++ program at `/home/user/calc_ci.cpp` to read this filtered data (either from a file you create or via standard input) and calculate the mean and the 95% confidence interval for the `accuracy` metric. 
   - Use the sample standard deviation for your calculations.
   - Use a Z-score of `1.96` for the 95% confidence interval.
4. Compile your C++ program and run it to produce the final output. Save the output to `/home/user/ci_output.txt` in the exact following format, with values rounded to 4 decimal places:
`Mean: X.XXXX, CI: [Y.YYYY, Z.ZZZZ]`

Example output format:
`Mean: 0.8200, CI: [0.8061, 0.8339]`