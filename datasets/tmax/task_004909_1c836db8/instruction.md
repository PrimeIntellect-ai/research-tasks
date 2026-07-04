You are an ML Engineer preparing a robust training dataset from a noisy, large-scale CSV file. You need to perform feature selection based on hypothesis testing and balance the classes using bootstrap resampling.

You have been provided a dataset at `/home/user/data/raw_data.csv`. The file has the following header: `id,label,f1,f2,...,f20`. The `label` column contains binary classes (`0` or `1`).

Your task is to write a C++ program (and any necessary build scripts like a `Makefile` or `CMakeLists.txt`) to process this data. The C++ program must accomplish the following:

1. **Feature Selection via Hypothesis Testing**:
   For each feature `f1` through `f20`, compute the Welch's t-statistic between the two groups defined by `label == 0` and `label == 1`. 
   The formula for the absolute t-statistic is:
   `|t| = |mean_1 - mean_0| / sqrt((var_1 / n_1) + (var_0 / n_0))`
   *(Note: Use the unbiased sample variance, divided by n-1, for `var_1` and `var_0`).*
   Identify the top 3 features with the highest absolute t-statistic.

2. **Bootstrap Resampling**:
   Using the selected 3 features, create a new balanced dataset via bootstrap resampling (sampling *with replacement*).
   - Sample exactly 1000 records where `label == 0`.
   - Sample exactly 1000 records where `label == 1`.
   - **Crucial**: To ensure reproducibility, use `std::mt19937` initialized with the seed `42` for your random number generation. Use `std::uniform_int_distribution<size_t>` to pick indices. Generate the 1000 class `0` samples first (using indices from the filtered class `0` array), then generate the 1000 class `1` samples. Maintain the original relative order of the classes in memory as they appeared in the CSV when creating your filtered arrays.

3. **Output Generation**:
   - Write the newly sampled 2000 rows to `/home/user/data/prepared_data.csv`. The header must be exactly `id,label,<top1_feature_name>,<top2_feature_name>,<top3_feature_name>` where the feature names are ordered by descending absolute t-statistic.
   - Write a log file to `/home/user/data/metrics.txt` containing the top 3 features and their absolute t-statistics formatted to exactly 4 decimal places. 
   Format of `metrics.txt`:
   ```
   <feature_name>: <t-stat>
   <feature_name>: <t-stat>
   <feature_name>: <t-stat>
   ```

Write, compile, and run your C++ pipeline. You may use standard Bash commands to set up your directories or compile your code. You may only use the C++ Standard Library. No external libraries (like Boost or Eigen) are permitted.