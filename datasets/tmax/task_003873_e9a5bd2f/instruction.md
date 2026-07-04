You are acting as a Data Scientist handling system telemetry logs. You have been provided with a raw dataset of system metrics at `/home/user/system_metrics.csv`. The dataset contains various continuous features and a binary target variable `is_anomaly`. 

Your objective is to clean the dataset, perform correlation analysis, train a probabilistic classification model, and deploy it as a local microservice.

Perform the following steps:

1. **Environment Setup**:
   Install any necessary Python libraries (e.g., `pandas`, `scikit-learn`, `flask`, `numpy`) in your user environment. Do not use `sudo`.

2. **Data Cleaning & Imputation**:
   - Read the dataset `/home/user/system_metrics.csv`.
   - Drop any rows where the target column `is_anomaly` is missing (NaN).
   - For all other missing values in the continuous feature columns, impute them using the median value of that specific column (computed over the remaining training data).

3. **Correlation Analysis**:
   - Compute the Pearson correlation matrix for the features (excluding the target `is_anomaly`).
   - Identify pairs of features that have an absolute correlation strictly greater than `0.85`.
   - To remove redundant information, drop one feature from each highly correlated pair. Specifically, between the two correlated features, **drop the one that appears last alphabetically**. Apply this rule iteratively or simultaneously, but ensure that no remaining pair has an absolute correlation > 0.85.

4. **Bayesian Modeling**:
   - Using the cleaned, reduced feature set, train a Gaussian Naive Bayes classifier (`GaussianNB` from `scikit-learn`) to predict `is_anomaly`.

5. **Model Deployment (API)**:
   - Write a Python script (`/home/user/serve_model.py`) that runs a Flask web service on `127.0.0.1` port `8080`.
   - Create an endpoint `POST /predict`.
   - The endpoint must accept a JSON payload containing the remaining (retained) features. Example: `{"cpu_load": 45.2, "disk_io": 12.0, ...}`
   - The endpoint must return a JSON response with exactly two keys:
     - `"anomaly_probability"`: The predicted probability that the input is an anomaly (class 1) as a float (using the model's `predict_proba` method).
     - `"is_anomaly"`: The predicted class label as an integer (0 or 1).
   - Start the service in the background and ensure it is actively listening on port 8080. Leave it running.

Your final deliverable is the running Flask service on port 8080 that successfully processes incoming prediction requests according to the rules above.