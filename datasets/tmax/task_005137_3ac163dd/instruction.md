You are an AI assistant helping a data science researcher organize and evaluate dataset metadata. The researcher has built a custom Python package for data preprocessing and a pipeline for classifying datasets. However, the pipeline is exhibiting data leakage, and the deployment needs to be finalized.

Your task has three parts:

1. **Fix the Preprocessing Package:**
There is a vendored Python package located at `/app/vendored/datacleaner-1.0.0`. It contains a bug in `datacleaner/core.py` within the `prepare_and_split` function. The function currently applies a `StandardScaler` to the entire feature set *before* performing the train/test split. This causes data leakage from the test set into the training set. 
Modify the `prepare_and_split(X, y, test_size, random_state)` function so that it first splits the data using `train_test_split`, and *then* fits the scaler ONLY on the training data, applying the transformation to both the training and test sets. Return `X_train_scaled, X_test_scaled, y_train, y_test`. After fixing it, reinstall or ensure the package is usable by your environment.

2. **Train the Classification Model:**
Using the fixed `datacleaner` package, write a script to load the dataset `/home/user/data/raw_datasets.csv`. The dataset has columns `num_samples`, `num_features`, `missing_ratio`, `variance_score`, and a target column `category` (integer). 
Split the data using `test_size=0.2` and `random_state=42`. Train a `RandomForestClassifier(random_state=42)` from scikit-learn on the training set. Save the trained model to `/home/user/model.pkl` and the fitted scaler to `/home/user/scaler.pkl` (make sure your fixed `prepare_and_split` function also returns the fitted scaler, e.g., returning a 5-tuple: `X_train_scaled, X_test_scaled, y_train, y_test, scaler`).
Additionally, perform a brief inference benchmark: time how long it takes to predict the entire test set 100 times in a loop. Save this benchmark metric in a JSON file at `/home/user/metrics.json` with the key `"inference_time_seconds"`.

3. **Serve the Model:**
Create and start a web service (using Flask, FastAPI, or similar) that listens on `127.0.0.1:8080`.
The service must expose a POST endpoint at `/predict` that accepts JSON payloads in the format: `{"features": [num_samples, num_features, missing_ratio, variance_score]}`.
The endpoint MUST require an Authorization header: `Authorization: Bearer RESEARCH-SEC-2024`. If the token is missing or incorrect, return a 401 status code.
If authenticated, the service should scale the input features using the loaded `/home/user/scaler.pkl` and predict the category using `/home/user/model.pkl`. It should return a JSON response: `{"prediction": <integer_class>}`.

Leave the service running in the background. Do not stop it.