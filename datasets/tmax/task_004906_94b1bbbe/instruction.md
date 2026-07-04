You are a machine learning engineer tasked with preparing a training data pipeline and evaluating a baseline model. You need to orchestrate this process using a master Bash script.

You have been provided with a dataset at `/home/user/raw_data.csv`. It contains 1000 rows (plus a header) and 21 columns (`id`, `feature_1` to `feature_19`, and `target`). 

Your objective is to write an end-to-end pipeline that performs dimensionality reduction, Bayesian modeling, and numerical accuracy testing. 

Please perform the following steps:

1. **Create Python Scripts**:
   - `pca_transform.py`: Reads a training CSV and a testing CSV. It should fit a Principal Component Analysis (PCA) model on the training features (excluding `id` and `target`) to reduce them to exactly 3 components (use `random_state=42`). It should then transform both the training and testing features. Output the transformed datasets (including the original `id` and `target` columns) as `train_pca.csv` and `test_pca.csv`.
   - `bayesian_train_predict.py`: Reads `train_pca.csv` and `test_pca.csv`. It should train a `BayesianRidge` regressor (from `sklearn.linear_model`) on the training data (features = 3 PCA components, target = `target`). Then, it should predict the target values for the test data. Output a CSV named `predictions.csv` with exactly two columns: `id` and `predicted_target`.

2. **Create the Master Bash Script (`/home/user/run_pipeline.sh`)**:
   - This script must be executable.
   - It should first split `/home/user/raw_data.csv` into a training set and a testing set. 
     - `train_raw.csv` should contain the header and the first 800 data rows.
     - `test_raw.csv` should contain the header and the remaining 200 data rows.
   - It should execute `pca_transform.py` passing `train_raw.csv` and `test_raw.csv` as arguments (or hardcoded, as long as it runs them).
   - It should execute `bayesian_train_predict.py`.
   - **Numerical Accuracy Testing**: Finally, using Bash commands (like `awk`, `join`, or `bc`), the script must calculate the Mean Squared Error (MSE) between the `predicted_target` in `predictions.csv` and the actual `target` from `test_raw.csv`. 
   - Round the final MSE to exactly 2 decimal places and write ONLY this numeric value to `/home/user/mse_result.txt`.

Ensure your Bash script handles the headers correctly when splitting files and calculating the MSE. All scripts should be placed in `/home/user/`. Execute your `run_pipeline.sh` script to produce the final output before finishing.