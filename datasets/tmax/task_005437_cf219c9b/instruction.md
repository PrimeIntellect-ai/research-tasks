You are a data engineer building an ETL pipeline to process sensor data, perform dimensionality reduction, verify numerical accuracy, and train a baseline regression model.

Your task is to write and execute a Python script that performs the following steps on the dataset located at `/home/user/sensor_data.csv`:

1. **Data Loading & Preprocessing**:
   - Read the dataset. The first 50 columns (`f0` to `f49`) are features, and the last column (`target`) is the target variable.
   - Standardize the 50 features such that each feature has a mean of 0 and a standard deviation of 1 (use `sklearn.preprocessing.StandardScaler`).

2. **Dimensionality Reduction**:
   - Apply Principal Component Analysis (PCA) to the standardized features. Initialize PCA with `random_state=42`.
   - Determine `k`, the minimum number of principal components required to explain at least 95% (0.95) of the total variance.
   - Write the integer value of `k` to a file named `/home/user/n_components.txt`.

3. **Numerical Accuracy Testing**:
   - To ensure the PCA implementation is numerically stable, reconstruct the standardized features using **all 50** principal components (via the inverse transform).
   - Calculate the maximum absolute error between any element in the original standardized features and the reconstructed features.
   - Write this maximum absolute error to a file named `/home/user/pca_max_error.txt` in scientific notation (e.g., `1.234567e-15`).

4. **Regression Modeling**:
   - Transform the standardized features using only the `k` components you identified earlier.
   - Train a Ridge regression model (`sklearn.linear_model.Ridge` with `alpha=1.0`) on these `k` components to predict the `target` variable.
   - Predict the target for the same dataset and calculate the Mean Squared Error (MSE).
   - Write the MSE to a file named `/home/user/mse.txt`, rounded to exactly 4 decimal places.

Ensure all output files are created in the `/home/user/` directory as specified.