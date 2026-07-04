You are an AI assistant helping a systems researcher organize and analyze a dataset of server metrics. The researcher has collected telemetry from various servers, but the data is messy, contains sensor errors, and is highly dimensional. 

The raw dataset is located at `/home/user/system_metrics.csv`. It contains the following columns: `cpu_usage`, `mem_usage`, `disk_io`, `net_in`, `net_out`, and a binary target column `crashed` (1 if the server crashed, 0 otherwise).

Your task is to write and execute a Python script that processes this data and evaluates a probabilistic model. Follow this exact pipeline:

1. **Missing Value & Outlier Handling**:
   - Read `/home/user/system_metrics.csv`.
   - For all five feature columns (`cpu_usage`, `mem_usage`, `disk_io`, `net_in`, `net_out`), fill any missing values (NaN) with the median of that specific column (computed ignoring NaNs).
   - After imputation, handle extreme outliers by applying Winsorization: for each feature column, cap all values at the 99th percentile of that column. (i.e., any value greater than the 99th percentile should be replaced by the exact 99th percentile value).

2. **Dimensionality Reduction**:
   - Standardize the five cleaned feature columns so that each has a mean of 0 and a variance of 1 (using `StandardScaler`).
   - Apply Principal Component Analysis (PCA) to reduce the 5 features down to exactly 2 principal components. Use `random_state=42` if your PCA implementation accepts one.

3. **Bayesian Inference Modeling**:
   - Train a Gaussian Naive Bayes model (`GaussianNB` from scikit-learn) using the 2 principal components as inputs to predict the `crashed` target variable.
   - Train the model on the *entire* dataset.

4. **Model Output Validation**:
   - Predict the *probabilities* of crashing for the entire dataset using your trained GaussianNB model.
   - Validate the probabilistic outputs by calculating the Brier Score Loss (`brier_score_loss` from scikit-learn) between the true `crashed` labels and the predicted probability of the positive class (class 1).

5. **Reporting**:
   - Output the results of your analysis to a JSON file located at `/home/user/report.json`.
   - The JSON file must have exactly this structure, with float values rounded to exactly 4 decimal places:
     ```json
     {
       "imputed_cpu_median": <float>,
       "pca_explained_variance_ratio": [<float>, <float>],
       "brier_score": <float>
     }
     ```

You may install any necessary Python packages (like pandas, numpy, scikit-learn) using pip. Do not modify the original CSV file.