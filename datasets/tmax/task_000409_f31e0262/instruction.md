You are a data engineer working on optimizing an ETL pipeline. One of the bottleneck transformations involves heavy matrix operations. We need to determine if increasing the number of OpenMP/OpenBLAS threads significantly improves the inference performance of this transformation.

A standalone benchmark script simulating this transformation is located at `/home/user/transform_step.py`. When run, it performs the matrix operations and prints a single float to standard output representing the execution time in seconds.

Your task is to write a Python script at `/home/user/evaluate_etl.py` that does the following:
1. Installs any necessary numerical and statistical packages (e.g., `numpy`, `scipy`) if they are not already installed.
2. Programmatically executes `/home/user/transform_step.py` exactly 20 times with the environment variables `OMP_NUM_THREADS=1` and `OPENBLAS_NUM_THREADS=1`. Collect the printed times.
3. Programmatically executes the script exactly 20 times with the environment variables `OMP_NUM_THREADS=4` and `OPENBLAS_NUM_THREADS=4`. Collect the printed times.
4. Performs a two-sided Welch's t-test (independent t-test with unequal variances) to compare the mean execution times of the two configurations.
5. Calculates the 95% confidence interval for the difference in means (`mean(1_thread) - mean(4_thread)`).
6. Saves the statistical results to a JSON file exactly at `/home/user/benchmark_results.json` with the following keys:
   - `"mean_diff"`: The difference between the sample means (float).
   - `"t_statistic"`: The calculated t-statistic (float).
   - `"p_value"`: The two-sided p-value (float).
   - `"reject_null"`: A boolean indicating if we reject the null hypothesis at $\alpha = 0.05$.

Make sure your script runs end-to-end and outputs the JSON file correctly formatted. You should run the script yourself to verify it works.