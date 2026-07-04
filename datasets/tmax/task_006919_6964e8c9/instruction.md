You are an AI assistant acting as a data engineer. You are building an automated validation step for a C++ based ETL pipeline.

A recent ETL process has output a CSV file located at `/home/user/etl_output.csv`. The file has a header `val1,val2` followed by several hundred rows of floating-point numbers. We need to validate if the Pearson correlation coefficient between these two variables matches an expected baseline correlation, taking into account sampling variance. 

Your task is to write a standalone C++17 program that calculates the correlation, performs bootstrap resampling to compute a 95% confidence interval, and outputs a JSON validation report.

Write the C++ source code to `/home/user/validate_etl.cpp`. The program must:
1. Accept 4 command-line arguments: `<csv_file_path> <expected_correlation> <num_bootstraps> <rng_seed>`
2. Parse the CSV file (ignoring the header row).
3. Calculate the point estimate of the Pearson correlation coefficient ($r$) between `val1` and `val2`.
4. Perform bootstrap resampling to find the 95% confidence interval for the correlation:
   - Run `<num_bootstraps>` iterations.
   - In each iteration, create a bootstrap sample by sampling $N$ pairs with replacement from the original dataset (where $N$ is the total number of data rows).
   - Use `std::mt19937` initialized with `<rng_seed>` for random number generation.
   - To pick a random row index, use `std::uniform_int_distribution<int> dist(0, N - 1);`. Generate $N$ indices per bootstrap iteration in a loop.
   - Calculate the Pearson correlation for the bootstrap sample and store it.
5. Sort the bootstrap correlations in ascending order.
6. Calculate the 95% confidence interval boundaries. Use 0-based indexing: 
   - Lower bound index: `floor(0.025 * num_bootstraps)`
   - Upper bound index: `floor(0.975 * num_bootstraps)`
7. Check if the `<expected_correlation>` falls strictly within `[lower_bound, upper_bound]`. If it does, the status is `"VALID"`, otherwise `"INVALID"`.
8. Output a strictly formatted JSON string to standard output, exactly matching this structure (round floats to 4 decimal places):
```json
{
  "status": "VALID",
  "r_point": 0.8123,
  "ci_lower": 0.7900,
  "ci_upper": 0.8300
}
```

Once you have written the C++ code, compile it using `g++ -std=c++17 -O3 validate_etl.cpp -o validate_etl`.
Then, run the compiled program with the following parameters and redirect the output to `/home/user/validation_result.json`:
- CSV File: `/home/user/etl_output.csv`
- Expected correlation: `0.75`
- Number of bootstraps: `2000`
- RNG Seed: `42`

Use only the standard C++ library (no external libraries like Boost).