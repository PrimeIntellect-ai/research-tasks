You are an MLOps engineer tasked with building a reproducible, tracked pipeline for custom dimensionality reduction and inference benchmarking. 

You must implement a custom Principal Component Analysis (PCA) algorithm using raw linear algebra operations, benchmark its projection inference time, and track the experiments using MLflow.

Here are your instructions:

1. **Environment Setup:**
   - Create a Python virtual environment at `/home/user/venv`.
   - Install `numpy`, `pandas`, and `mlflow`.
   - A dataset already exists at `/home/user/data/matrix.csv` (contains purely numerical features, no header, comma-separated).

2. **Pipeline Development (`/home/user/run_experiment.py`):**
   - Write a reproducible Python script that takes a single integer argument `k` (the number of principal components).
   - **Linear Algebra Constraint:** You must implement PCA entirely from scratch using `numpy.linalg.svd`. Do NOT use `sklearn` or any other ML library.
   - The script must perform the following steps:
     a. Load the data from `/home/user/data/matrix.csv`.
     b. Mean-center the data.
     c. Compute the Singular Value Decomposition (SVD) of the centered data.
     d. Extract the projection matrix $W$ (shape: `num_features \times k`) containing the top `k` right singular vectors.
     e. Calculate the Reconstruction Mean Squared Error (MSE) over the entire dataset. (Reconstruction = Projected data transformed back to the original space + the original mean).

3. **Inference Benchmarking:**
   - Within the same script, benchmark the *inference time* (the time it takes to project the centered dataset using matrix multiplication with $W$).
   - Run this projection operation in a loop 1000 times.
   - Calculate the average time per projection across the 1000 runs (in seconds).

4. **Experiment Tracking (MLflow):**
   - Configure MLflow in your script to use a local tracking URI: `file:///home/user/mlruns`.
   - Set the MLflow experiment name to exactly `"PCA_Benchmarking"`.
   - For a given run, log the following to MLflow:
     - **Parameter:** `k` (the number of components used).
     - **Metric:** `mse` (the reconstruction Mean Squared Error).
     - **Metric:** `avg_inference_time_sec` (the average projection time from the benchmark).
     - **Artifact:** Save the projection matrix $W$ as a numpy `.npy` file named `projection_matrix.npy` and log it as an artifact for the run.

5. **Execution:**
   - Run your script three times to track three separate experiments, using $k = 2$, $k = 5$, and $k = 10$.

Verify your own success by checking that `/home/user/mlruns` is populated and contains the runs with the correct metrics and artifacts.