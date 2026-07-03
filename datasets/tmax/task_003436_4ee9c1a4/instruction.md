You are an ML Engineer preparing training data for a real estate pricing model. The raw dataset contains high-cardinality categorical variables (ZIP codes) that need to be encoded using empirical Bayes target encoding to prevent overfitting on ZIP codes with very few samples. You also need to track this feature engineering step using MLflow.

Here are your instructions:

1. **Environment Setup**:
   - Install `mlflow` and `pandas` if they are not already installed.
   - Start a local MLflow tracking server in the background bound to `127.0.0.1` on port `5000`. 
   - Ensure the server is running and accessible before proceeding.

2. **Bayesian Feature Engineering**:
   - Read the raw dataset located at `/home/user/raw_housing.csv`.
   - Implement Empirical Bayes Target Encoding for the `zip_code` column based on the target variable `price`.
   - Calculate the `zip_code_encoded` for each row using the following smoothing formula:
     `smoothed_mean = (n * mean_price + m * global_mean) / (n + m)`
     Where:
     * `n` = number of rows for that specific `zip_code`
     * `mean_price` = average `price` for that specific `zip_code`
     * `global_mean` = average `price` across the entire dataset
     * `m` = 15 (the smoothing weight prior)
   - Add this `zip_code_encoded` column to the dataframe. Keep all original columns.

3. **Experiment Tracking**:
   - Write a Python script (e.g., `process_data.py`) to perform the above operations.
   - In your script, set the MLflow tracking URI to `http://127.0.0.1:5000`.
   - Start an MLflow run with the name "Bayesian_Encoding".
   - Log the smoothing weight (`m=15`) as an MLflow parameter named `smoothing_weight`.
   - Log the `global_mean` as an MLflow metric named `global_mean_price`.

4. **Output**:
   - Save the transformed dataframe to `/home/user/processed_housing.csv` (keep the header, comma-separated).
   - Log the `/home/user/processed_housing.csv` file as an artifact in your MLflow run.

Ensure your script runs successfully, the MLflow server logs the experiment, and the final CSV is exactly at `/home/user/processed_housing.csv`.