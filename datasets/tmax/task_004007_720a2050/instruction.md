You are an MLOps engineer tasked with benchmarking a new high-performance approximation model against a ground-truth mathematical model. Both models have been provided to you, but you need to write a rigorous benchmarking and experiment tracking pipeline to validate the new model's performance, numerical accuracy, and output consistency.

Setup:
You have two Python files located in `/home/user/models/`:
1. `/home/user/models/ground_truth.py` containing `def compute_true(x: np.ndarray) -> np.ndarray`
2. `/home/user/models/fast_approx.py` containing `def compute_approx(x: np.ndarray) -> np.ndarray`

Your task is to create a Python script at `/home/user/benchmark.py` that performs the following steps:

1. **Test Data Generation:**
   - Create a test array `x` of exactly 1,000,000 evenly spaced points between `0.0` and `100.0` (inclusive) using NumPy, with dtype `np.float64`.

2. **Model Output Validation:**
   - Run both `compute_true(x)` and `compute_approx(x)`.
   - Verify that the outputs of both functions exactly match the input shape `(1000000,)` and the input dtype `np.float64`. Store this validation result as a boolean.

3. **Numerical Accuracy Testing:**
   - Calculate the Mean Squared Error (MSE) between the ground truth and the approximation.
   - Calculate the Maximum Absolute Error (Max Abs Error) between the ground truth and the approximation.

4. **Inference Performance Benchmarking:**
   - Measure the execution time of `compute_true(x)` and `compute_approx(x)`.
   - For each model, perform 10 consecutive executions and calculate the average execution time in milliseconds (ms).
   - Calculate the relative speedup: `(average ground truth time) / (average approximation time)`.

5. **Experiment Tracking:**
   - Save the results to an experiment log file at `/home/user/experiment_log.json`.
   - The JSON file must contain exactly the following keys and appropriate numerical/boolean values:
     - `"valid_shape_dtype"`: (bool) True if both outputs have the correct shape and dtype.
     - `"mse"`: (float) Mean Squared Error.
     - `"max_abs_error"`: (float) Maximum Absolute Error.
     - `"true_time_ms"`: (float) Average execution time of ground truth in ms.
     - `"approx_time_ms"`: (float) Average execution time of approximation in ms.
     - `"speedup"`: (float) Speedup ratio.

Execute your benchmarking script to generate the JSON log file.