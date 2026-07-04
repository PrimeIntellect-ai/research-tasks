You are a Data Engineer tasked with fixing a severe data leakage bug in a C++ ETL and inference pipeline, and then tracking the experiment results. 

A previous engineer wrote a C++ pipeline that reads time-series sensor data, normalizes it using Z-score scaling, and runs a simple regression model. However, they made a critical error: the Z-score normalization computes the mean and standard deviation using the *entire* dataset. This causes future data to leak into past predictions, invalidating the model's performance in production.

Your task has three parts:

1. **Fix the Data Leakage:**
   Navigate to `/home/user/pipeline/`. You will find a C++ project. 
   Modify the `compute_zscore` function in `/home/user/pipeline/src/processor.cpp`. 
   Change the implementation so that for an element at index `i`, the Z-score is calculated using an **expanding window** (i.e., the mean and sample standard deviation of elements strictly from index `0` to `i-1`). 
   *Note:* Use sample standard deviation (divide by N-1). If `i=0` or `i=1` (where sample std dev is undefined or 0), the normalized value should simply be `0.0`.

2. **Implement Correlation Analysis:**
   In the same file, implement the `compute_pearson_correlation` function to calculate the Pearson correlation coefficient between two vectors of equal length.

3. **Build, Run, and Track:**
   - Build the C++ project using CMake in the `/home/user/pipeline/build/` directory.
   - Run the executable: `./etl_pipeline /home/user/data/sensor_data.csv`.
   - The program will automatically generate `/home/user/pipeline/build/predictions.csv`.
   - Create an experiment tracking log at `/home/user/experiment_log.json`. It must be valid JSON matching this exact format:
     ```json
     {
       "experiment_name": "fix_data_leakage",
       "pearson_correlation_feature1_feature2": <float_value_from_stdout>
     }
     ```
     The C++ program will print the correlation value to stdout when run. Use that exact printed value (to 4 decimal places) in the JSON file.

Ensure your C++ code compiles without errors using standard CMake commands (`cmake .. && make`). Do not modify `main.cpp` or `CMakeLists.txt`.