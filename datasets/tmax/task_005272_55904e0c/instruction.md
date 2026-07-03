You are a data analyst working on a custom threshold-based classifier written in Rust. You need to evaluate the cross-validation results of different hyperparameters, validate the model's performance, and benchmark its inference speed.

Your workspace is in `/home/user/model_eval`. You have two datasets:
1. `/home/user/model_eval/cv_results.csv` - Contains the cross-validation predictions for different hyperparameter values (`k`). 
   Columns: `fold_id`, `k`, `y_true`, `y_pred`
2. `/home/user/model_eval/inference_data.csv` - Contains new data for benchmarking inference.
   Columns: `id`, `feature_val`

Your task is to create and run a Rust program in `/home/user/model_eval` (initialize a cargo project here if needed, or just write a script) that performs the following:

**1. Cross-Validation and Hyperparameter Tuning**
Parse `cv_results.csv`. For each hyperparameter `k`, calculate the accuracy of the predictions (`y_true == y_pred`) within each `fold_id`. Then, compute the cross-validated accuracy for each `k` by taking the average of its fold accuracies. 
Identify the `best_k` that has the highest cross-validated accuracy.

**2. Model Output Validation**
Validate that the cross-validated accuracy of the `best_k` is greater than or equal to `0.80`. If no `k` meets this threshold, the program should gracefully exit with a non-zero status code.

**3. Inference Performance Benchmarking**
Load all `feature_val` entries from `inference_data.csv` into memory (e.g., a `Vec<f64>`). 
Write a benchmark loop that applies the threshold classifier to all loaded features 1,000 times. 
The classifier logic is: `prediction = if feature_val > best_k { 1 } else { 0 }`.
Measure the *total* time it takes to run this loop 1,000 times across the entire dataset (do not include CSV parsing time in this benchmark).

**4. Reporting**
Output the results to `/home/user/model_eval/report.json` with the exact following JSON structure:
```json
{
  "best_k": 5.0,
  "cv_accuracy": 0.852,
  "benchmark_time_us": 123456
}
```
*(Note: Use the actual values computed. The time can be an integer in microseconds).*

Requirements:
- Write the logic entirely in Rust.
- You may use the `csv` and `serde` crates (and any other standard/common crates you wish to add to `Cargo.toml`).
- Ensure the final JSON file is strictly formatted.