You are acting as an MLOps engineer managing an artifact tracking system. We have a C++ ETL pipeline that processes model experiment metrics. Currently, the pipeline exhibits a critical data leakage bug and lacks statistical verification.

There are three datasets located in `/home/user/`:
1. `train_metrics.csv` (Columns: `experiment_id,loss_score`)
2. `test_metrics.csv` (Columns: `experiment_id,loss_score`)
3. `metadata.csv` (Columns: `experiment_id,duration_seconds`)

The existing C++ code is at `/home/user/etl_pipeline.cpp`. It reads the CSV files, joins the metrics with metadata using `experiment_id`, and performs Z-score normalization on the `loss_score` column. 

**Your Tasks:**
1. **Fix the Data Leak:** The current C++ code concatenates the train and test data *before* calculating the mean and standard deviation for normalization. This leaks information from the test set into the training preprocessing. Modify `/home/user/etl_pipeline.cpp` so that the mean and standard deviation are calculated **strictly on the training data**, but then applied to normalize both the training and test sets.
2. **Add Statistical Analysis:** Extend the C++ code to compute the 95% Confidence Interval for the mean of the *normalized test set loss scores*. Use the standard normal distribution (Z = 1.96) for this calculation. Formula: `Mean ± 1.96 * (Standard Deviation of Normalized Test Set / sqrt(N))`
3. **Output:** The C++ program must write exactly the confidence interval to a file named `/home/user/test_ci.txt` in the format: `[lower_bound, upper_bound]` (e.g., `[0.1234, 0.5678]`), rounded to 4 decimal places.
4. Compile your fixed code using `g++ -O3 -std=c++17 /home/user/etl_pipeline.cpp -o /home/user/etl_pipeline` and run it.

Ensure your pipeline processes the join correctly (only keeping records present in both the metrics and metadata files) before performing the normalization and statistical calculations.