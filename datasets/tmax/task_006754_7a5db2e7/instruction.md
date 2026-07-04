You are a data analyst who needs to process experimental data and compute statistical confidence intervals. Because performance is critical for the pipeline, you need to implement the core bootstrap algorithm in C using the GNU Scientific Library (GSL).

We have an experiment dataset located at `/home/user/data/experiment.csv` with the following columns: `id,measurement_a,measurement_b,category`.

Your task:
1. Ensure the necessary C development libraries for GSL are installed on the system (you have `sudo` access to run package managers like `apt` if needed, but assume you are the user `user`).
2. Write a C program at `/home/user/bootstrap_ci.c` that does the following:
   - Reads the CSV file `/home/user/data/experiment.csv`.
   - Filters the dataset to include only rows where `category` is exactly `X`.
   - Extracts the values from the `measurement_b` column for these filtered rows.
   - Performs a bootstrap resampling (with replacement) to compute the 95% Confidence Interval for the mean of the extracted `measurement_b` values.
   - You must use exactly `10000` bootstrap iterations.
   - You must use the GSL random number generator `gsl_rng_mt19937`.
   - You must initialize the RNG with the exact seed `42` (`gsl_rng_set(r, 42)`) for reproducibility. Use `gsl_rng_uniform_int(r, N)` to select indices, where N is the number of filtered rows.
   - Calculate the mean of each of the 10000 resamples.
   - Sort these means in ascending order.
   - The lower bound of the 95% CI is the 250th value (index 249 in a 0-indexed array).
   - The upper bound of the 95% CI is the 9750th value (index 9749 in a 0-indexed array).
3. Compile the C program to an executable located at `/home/user/bootstrap_ci`.
4. Run the program and append the result to an experiment tracking log file at `/home/user/experiment_log.txt`. 

The output appended to the log file must be exactly in this format (rounded to exactly 4 decimal places):
`Feature: measurement_b, Filter: category=X, CI_Lower: <val>, CI_Upper: <val>`

Make sure your C program handles compilation and linking against the GSL libraries correctly (`-lgsl -lgslcblas -lm`).