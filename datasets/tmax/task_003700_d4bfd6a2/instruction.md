You are a Machine Learning Engineer responsible for building a high-performance C++ ETL and evaluation pipeline for a new model. 

We have a dataset located at `/home/user/dataset.csv` containing three columns: `id`, `f1`, and `y`.
- `id` is an integer.
- `f1` is a very large 64-bit integer feature (values can be up to $2^{62}$). Some entries in this column are missing and are represented by the string `"NaN"`.
- `y` is a double-precision floating-point target.

Your task is to write a C++ program at `/home/user/ml_pipeline.cpp` that performs the following:

**1. ETL Pipeline & Imputation:**
Read the CSV file. You must impute the missing `"NaN"` values in `f1` with the exact integer mean of the valid `f1` values (truncated towards zero).
*Critical:* Because `f1` contains extremely large integers, you must be careful not to lose precision when summing or calculating the mean. Standard 64-bit integer summation may overflow, and casting to `double` will silently cause precision loss (similar to the silent `NaN` coercion issues in Pandas).

**2. Model Evaluation (Cross-Validation / Tuning):**
You need to evaluate three predefined candidate linear models to find the one with the lowest Mean Squared Error (MSE) on the fully imputed dataset. The predictions are calculated as `y_pred = f1 * weight + bias`.
*   **Model 1:** weight = `1.2e-10`, bias = `0.5`
*   **Model 2:** weight = `1.5e-10`, bias = `-0.2`
*   **Model 3:** weight = `1.3e-10`, bias = `0.1`

Calculate the MSE for each model using double precision.

**3. Performance Benchmarking:**
To benchmark inference speed, simulate a load test by computing the predictions of the *best* model over the entire imputed dataset 1,000 times in a loop. Measure the total time taken for these 1,000 passes.

**4. Reporting:**
Your program should output a report to `/home/user/report.txt` containing exactly the following four lines:
```text
Imputed Mean: <exact_integer_mean>
Best Model: <1, 2, or 3>
Best MSE: <MSE_rounded_to_4_decimal_places>
Benchmark Time: <total_time_in_milliseconds> ms
```
*(Note: The benchmark time does not need to be exact for the automated tests, but the format must match).*

Compile your code using `g++ -O3 -std=c++17 /home/user/ml_pipeline.cpp -o /home/user/ml_pipeline` and run it to produce the report.