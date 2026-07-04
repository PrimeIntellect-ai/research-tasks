You are a data analyst working on a C++ data pipeline. We have a dataset of user records in `/home/user/data.csv`. The pipeline is supposed to read the data, filter out invalid rows, and compute bootstrap statistics. However, our previous pipeline silently parsed missing or malformed fields as zeros, which skewed our analysis. 

Your task is to write a strictly reproducible C++ program that enforces the schema, samples the data, and computes a confidence interval.

**Requirements:**
1. **Schema Enforcement:** 
   Read `/home/user/data.csv`. The file has no header. Every row must have exactly three columns: `id` (integer), `age` (integer), and `score` (float). 
   If a row has missing values (e.g., `1,,5.0`), non-numeric characters, or extra columns, it must be completely ignored.

2. **Reproducible Bootstrap Pipeline:**
   Extract the valid `score` values into an array/vector. Let `N` be the number of valid rows.
   Perform a bootstrap analysis with exactly `10,000` iterations to estimate the mean score.
   - For each iteration, draw `N` samples **with replacement** from the valid scores.
   - Use `std::mt19937` initialized with the seed `42`. 
   - Use `std::uniform_int_distribution<size_t>(0, N - 1)` to generate the random indices for sampling.

3. **Output Generation:**
   Compute the mean of each of the 10,000 bootstrap samples.
   Sort these 10,000 means to find the 95% Confidence Interval (use the 2.5th percentile and 97.5th percentile, which correspond to indices 250 and 9749 in a 0-indexed sorted array).
   Compute the overall average of the 10,000 sample means.
   
   Write the results to `/home/user/bootstrap_results.txt` in exactly this format (rounded to 2 decimal places):
   ```
   Valid rows: <N>
   Mean: <X.XX>
   95% CI: [<L.LL>, <U.UU>]
   ```

Write your C++ code to `/home/user/bootstrap.cpp`, compile it (e.g., using `g++ -std=c++17 -O3`), and run it to produce the `bootstrap_results.txt` file.