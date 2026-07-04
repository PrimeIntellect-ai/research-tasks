You are a machine learning engineer preparing feature data for a new model. You need to analyze the covariance of your features and benchmark a mock inference operation using Go. 

A dataset of continuous features has been generated at `/home/user/features.csv`. It contains 100 rows and 3 columns of comma-separated float values, with no header row.

Your task is to build a Go pipeline in the directory `/home/user/ml_pipeline` to process this data.

Requirements:
1. Initialize a Go module named `ml_pipeline` in `/home/user/ml_pipeline`.
2. Write a Go program (`main.go`) that:
   - Reads `/home/user/features.csv`.
   - Uses the `gonum.org/v1/gonum/mat` and `gonum.org/v1/gonum/stat` packages to compute the unbiased covariance matrix of the 3 features.
   - Outputs the exact 3x3 covariance matrix to `/home/user/ml_pipeline/covariance.csv`. The output must be comma-separated, with each value formatted to exactly 6 decimal places (e.g., `1.234567`).
3. Write a Go benchmark in `pipeline_test.go` with a function named `BenchmarkInference`. 
   - The benchmark should simulate inference by calculating the dot product of the first row of features from the CSV and a static weight vector `[0.5, 0.5, 0.5]`. 
   - The benchmark must loop `b.N` times.
4. Run your Go program to generate `covariance.csv`.
5. Run your Go benchmark and save the raw standard output to `/home/user/ml_pipeline/benchmark.txt`.

Ensure all files are created exactly at the specified paths.