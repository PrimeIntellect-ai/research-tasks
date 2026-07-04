You are an MLOps engineer tracking experiment artifacts. You have been given a raw CSV log file from a recent model evaluation run, but the data is noisy. Some metrics failed to record (missing values), and some contain corrupted out-of-bounds metrics (outliers). 

Your task is to build a minimal C++ ETL pipeline that parses the CSV, cleans the data, and performs a statistical bootstrap to evaluate the performance of a specific model.

The raw data is located at `/home/user/experiments.csv`.

Write a C++ program at `/home/user/mlops_etl.cpp` that does the following:
1. **ETL & Data Cleaning:** 
   Read `/home/user/experiments.csv`. The CSV has a header: `id,model_name,accuracy,loss`.
   Filter the data to keep only rows where `model_name` is exactly `"BetaNet"`.
   Discard any rows that meet ANY of the following conditions:
   - `accuracy` or `loss` is empty or exactly `"NaN"`.
   - `accuracy` is less than `0.0` or greater than `1.0`.
   - `loss` is less than `0.0`.
   
2. **Bootstrap Sampling (Model Evaluation):**
   Extract the valid `accuracy` values for `BetaNet` in the order they appear.
   Perform a bootstrap analysis to compute the 95% confidence interval for the mean accuracy.
   - Set up your random number generator exactly as: `std::mt19937 gen(42);`
   - Create a distribution: `std::uniform_int_distribution<size_t> dist(0, N - 1);` where `N` is the number of valid `BetaNet` rows.
   - Generate `10000` bootstrap samples. Each bootstrap sample should consist of `N` draws (with replacement) from the valid accuracies.
   - For each bootstrap sample, compute its mean accuracy.
   - Store the 10000 sample means and sort them in ascending order.
   
3. **Reporting:**
   Calculate the "mean of means" (the average of your 10000 bootstrap sample means).
   Find the lower bound (2.5th percentile, index `250`) and upper bound (97.5th percentile, index `9750`) of the sorted means.
   Write the results to `/home/user/report.txt` with exactly the following format (round values to 4 decimal places):
   
   ```
   Model: BetaNet
   Valid Samples: <N>
   Mean of Means: <mean>
   95% CI: [<lower>, <upper>]
   ```

Compile your C++ program using standard C++17:
`g++ -std=c++17 /home/user/mlops_etl.cpp -o /home/user/mlops_etl`

Run the program so that it generates `/home/user/report.txt`.