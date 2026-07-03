You are helping a researcher debug and optimize a custom C++ machine learning pipeline. 

The researcher has implemented a basic Ridge Regression model with K-Fold cross-validation from scratch to tune the regularization hyperparameter (`alpha`). However, they suspect there is a subtle data leakage bug in the pipeline that is causing artificially inflated cross-validation scores. Additionally, they need to benchmark the inference performance of the model.

In `/home/user/ml_pipeline`, you will find:
- `main.cpp`: The source code for the pipeline.
- `Makefile`: To build the project.
- `dataset.csv`: A tabular dataset with 5 features and 1 target variable (the last column).

Your task has three parts:

1. **Fix the Data Leak**: 
   Currently, `main.cpp` computes the mean and standard deviation for feature scaling on the *entire dataset* before splitting it into cross-validation folds. This leaks information from the validation folds into the training process. Modify `main.cpp` so that for each fold, the mean and standard deviation are computed **only** on the training fold, and then those specific training statistics are used to scale both the training fold and the validation fold.

2. **Add Inference Benchmarking**:
   Modify `main.cpp` to measure the total inference time (the time taken to run the `predict` function on the validation fold) for each fold. Aggregate this to find the average inference time per fold in microseconds (us). Use `<chrono>` for high-resolution timing.

3. **Generate Results**:
   Compile the fixed code using the provided `Makefile`. Run the pipeline and save the results to a CSV file located exactly at `/home/user/ml_pipeline/benchmark_results.csv`.
   
   The output CSV must contain a header and have exactly this format:
   ```csv
   alpha,cv_mse,avg_inference_time_us
   0.1,2.345,15
   1.0,2.567,14
   10.0,3.123,16
   ```
   (Note: The actual numbers will depend on the fixed code's output. Ensure `cv_mse` is rounded to 3 decimal places).

Requirements:
- Only standard C++ libraries (e.g., `<iostream>`, `<vector>`, `<chrono>`, `<cmath>`, `<numeric>`) are permitted. Do not install external ML libraries.
- The compilation should be successful with `make`.
- The final output must be written to `/home/user/ml_pipeline/benchmark_results.csv`.