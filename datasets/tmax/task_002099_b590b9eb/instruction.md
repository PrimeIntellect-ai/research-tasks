You are tasked with fixing a flawed machine learning pipeline and optimizing its inference speed. 

A previous data scientist left behind a script, but it has two major issues:
1. **Data Leakage**: The dimensionality reduction (PCA) is being fitted on the entire dataset before the train-test split, leaking test set information into the training phase.
2. **Inefficient Inference**: The custom inference function for the model is written using slow Python `for` loops instead of optimized linear algebra operations.

Your goal is to write a reproducible Python script at `/home/user/run_pipeline.py` that fixes these issues and generates a report.

Here are the requirements for your script:
1. **Load the data**: Read `/home/user/data.csv`. The target variable is `y`, and all other columns are features.
2. **Train/Test Split**: Split the data using `test_size=0.2` and `random_state=42`.
3. **Pipeline Construction**: Create a scikit-learn pipeline (or appropriately sequential steps) that:
   - Applies `PCA(n_components=5, random_state=42)` ONLY on the training data.
   - Fits a `Ridge(alpha=1.0, random_state=42)` regression model.
4. **Vectorized Inference**: Write a function `fast_inference(model, X_test_transformed)` that computes the predictions using NumPy matrix multiplication (`@` or `np.dot`) and the model's `.coef_` and `.intercept_` attributes, strictly without using Python `for` loops or the built-in `.predict()` method.
5. **Benchmarking**: Measure the average time taken by your `fast_inference` function over 100 iterations on the test set.
6. **Output**: Your script must generate a JSON file at `/home/user/results.json` containing the following keys:
   - `"test_mse"`: The Mean Squared Error of your predictions on the test set (float).
   - `"avg_inference_time_sec"`: The average time taken for one inference pass on the test set, averaged over 100 runs (float).
   - `"predictions"`: A list of the first 10 predicted values on the test set (list of floats).

The dataset `/home/user/data.csv` is already present on the system. Do not modify it. Ensure your script handles dependencies appropriately.