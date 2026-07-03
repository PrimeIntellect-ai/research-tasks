You are a data analyst tasked with processing sensory data from two different sensors. The data has been collected into two separate CSV files:
1. `/home/user/sensor_x.csv` - Contains columns `id` and `val_x`
2. `/home/user/sensor_y.csv` - Contains columns `id` and `val_y`

Your task is to write a C++ pipeline that performs data joining, simple dimensionality reduction, and numerical accuracy testing via bootstrap sampling.

Perform the following steps:
1. Join the two datasets on the `id` column (inner join). Sort the joined dataset by `id` in ascending order to ensure deterministic processing.
2. Reduce the dimensionality of the joined (x, y) features by projecting them onto the 1D diagonal line. Specifically, compute the projection scalar for each row: `p_i = (val_x + val_y) / sqrt(2)`. Use double precision for all floating-point operations.
3. Write a C++ program (e.g., `analyze.cpp`) that calculates the sample mean of `p_i` across all matched records.
4. In the same C++ program, implement a bootstrap resampling procedure to estimate the standard error of this mean:
   - Perform exactly `B = 10000` bootstrap iterations.
   - For random number generation, initialize the standard Mersenne Twister with a seed of 42: `std::mt19937 gen(42);`.
   - To ensure cross-compiler reproducibility, do NOT use `std::uniform_int_distribution`. Instead, generate indices using the modulo operator: `size_t idx = gen() % n;` where `n` is the number of joined rows.
   - For each iteration, draw `n` samples with replacement from your projection scalars, and compute the mean of this bootstrap sample.
   - Calculate the sample standard deviation of these 10000 bootstrap means. This is your bootstrap standard error (use `B - 1` in the denominator for the variance calculation).
5. Output the results to `/home/user/bootstrap_results.txt` with exactly 6 decimal places of precision, in the following format:
```
Original Mean: <mean_value>
Bootstrap SE: <se_value>
```

Ensure your C++ code is compiled and executed, and the final output file exists with the correct values.