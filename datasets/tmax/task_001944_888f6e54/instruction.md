You are an AI assistant helping a data science researcher organize experimental sensor datasets, train a robust predictive model, and benchmark its inference performance.

Your tasks are to perform the following steps on a Linux system:

**Phase 1: ETL Pipeline & Data Transformation**
There is a raw dataset located at `/home/user/raw_sensors.csv`. The columns are `timestamp`, `sensor_id`, `temperature`, `vibration`, `pressure`, and `status`.
1. Write a Python script to load this CSV.
2. Sort the data by `sensor_id` and then by `timestamp` in ascending order.
3. For each `sensor_id`, calculate a 3-row rolling mean for `temperature`, `vibration`, and `pressure`. 
4. Drop any rows that contain NaN values as a result of the rolling window operation.
5. Save this processed dataset to `/home/user/processed_sensors.csv`.

**Phase 2: Model Training & Hyperparameter Tuning**
1. Using the processed dataset, train a `RandomForestClassifier` (from `scikit-learn`) to predict `status` using ONLY the three rolling mean features (`temperature`, `vibration`, `pressure`).
2. Perform hyperparameter tuning using `GridSearchCV` with 3-fold cross-validation (`cv=3`).
3. Use the following parameter grid:
   - `n_estimators`: [10, 50]
   - `max_depth`: [3, 5]
4. Set `random_state=42` for the RandomForestClassifier.
5. Save the best fitted model using `joblib` to `/home/user/best_model.joblib`.
6. Save the best parameters found by GridSearchCV as a JSON file at `/home/user/best_params.json` (e.g., `{"max_depth": 5, "n_estimators": 50}`).

**Phase 3: Model Serving & Inference Benchmarking**
1. Install `fastapi`, `uvicorn`, `scikit-learn`, `pandas`, `requests`, and `joblib`.
2. Write a FastAPI application in `/home/user/app.py` that loads `/home/user/best_model.joblib`.
3. Create a `POST /predict` endpoint that accepts a JSON payload of the form `{"temperature": float, "vibration": float, "pressure": float}` and returns `{"status": int}` (where `int` is the predicted class 0 or 1).
4. Run the FastAPI server in the background on port 8000.
5. Write a benchmarking script `/home/user/benchmark.py` that sequentially sends 100 HTTP POST requests to the `/predict` endpoint with dummy data `{"temperature": 0.5, "vibration": 0.5, "pressure": 0.5}`.
6. Once the benchmark script finishes successfully, it should create a file at `/home/user/benchmark_status.txt` containing the word `SUCCESS`.

Ensure your server remains running in the background so it can be tested.