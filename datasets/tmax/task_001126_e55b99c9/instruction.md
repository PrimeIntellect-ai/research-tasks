You are tasked with fixing a machine learning workflow that suffers from data leakage and improper validation. 

You need to write a Python script at `/home/user/pipeline/train_and_benchmark.py` that processes a dataset, trains a model using proper bootstrap sampling, and benchmarks the inference time.

A dataset is provided at `/home/user/pipeline/data.csv`. It contains several feature columns (`f1`, `f2`, `f3`, `f4`) and a target column (`target`).

Your script must perform the following steps exactly:

1. **Data Schema Enforcement**:
   - Read `/home/user/pipeline/data.csv`.
   - Drop any rows containing missing values (NaNs).
   - Ensure all feature columns (`f1` to `f4`) are explicitly cast to `float64`.

2. **Bootstrap Sampling & Train/Test Split**:
   - Set the random seed for reproducibility: `import numpy as np; np.random.seed(42)`
   - Create a bootstrap sample for the training set by sampling $N$ rows (where $N$ is the number of rows after cleaning) with replacement. Use `df.sample(frac=1.0, replace=True, random_state=42)`.
   - The Out-Of-Bag (OOB) samples (the rows from the cleaned dataset that were *not* selected in the bootstrap sample) must be used as the test set.

3. **Model Pipeline & Preventing Data Leakage**:
   - Create a scikit-learn `Pipeline` consisting of a `StandardScaler` followed by a `LinearRegression` model.
   - Train the pipeline on the bootstrap training set. **Crucially, ensure there is no data leakage.** The scaler must be fitted *only* on the training data, not on the entire dataset beforehand.

4. **Evaluation & Inference Benchmarking**:
   - Evaluate the pipeline by calculating the $R^2$ score on the OOB test set.
   - Benchmark inference performance: Run the pipeline's `predict` method on the OOB test set 100 times consecutively in a loop.
   - Calculate the *average* time it takes to predict the entire OOB set per iteration, in milliseconds.

5. **Output**:
   - Save a JSON file at `/home/user/pipeline/results.json` containing the evaluation and benchmark results.
   - The JSON must have exactly two keys:
     - `"oob_r2"`: The float $R^2$ score on the OOB set.
     - `"avg_inference_ms"`: The float representing the average inference time per OOB prediction pass in milliseconds.

Write the script and execute it so that `results.json` is generated.