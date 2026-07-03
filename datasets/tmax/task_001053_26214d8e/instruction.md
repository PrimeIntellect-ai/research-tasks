You are an AI assistant acting as a Data Engineer. You have been tasked with fixing and completing an ETL pipeline and machine learning service. 

In the `/app/services` directory, there is a `start.sh` script that brings up two upstream data APIs on ports 8001 and 8002.
- `http://127.0.0.1:8001/users` returns user data: `[{"user_id": int, "feature_1": float, "target": int}, ...]`
- `http://127.0.0.1:8002/transactions` returns transaction data: `[{"user_id": int, "feature_2": float}, ...]`

Your task is to build a new service, `model_service.py`, that must listen on `0.0.0.0:8080`. You can write it in any language, but Python (with FastAPI/Flask and scikit-learn) is recommended.

The service must:
1. Fetch data from both upstream APIs.
2. Join the data on `user_id` (Inner Join).
3. Preprocess the features (`feature_1` and `feature_2`) using standard scaling (zero mean, unit variance). 
4. Split the data into train and test sets (80% train, 20% test). **Crucial Requirement**: Ensure there is no data leakage between the train and test sets during scaling. The scaler must only be fitted on the training data.
5. Train a Gaussian Naive Bayes classifier (Bayesian probabilistic model) to predict `target` using the scaled `feature_1` and `feature_2`.
6. Calculate the accuracy of the model on the test set.

Your service must expose the following HTTP endpoints:
- `GET /metrics`: Returns a JSON response `{"test_accuracy": <float>}`. The float must be the exact accuracy on the test set (rounded to 4 decimal places).
- `POST /predict`: Accepts a JSON payload `{"feature_1": <float>, "feature_2": <float>}`. It must scale these features using the fitted scaler, predict the probability of class `1` using the Gaussian Naive Bayes model, and return `{"probability_class_1": <float>}` (rounded to 4 decimal places).

Requirements:
- You must set up your own analysis environment (e.g., installing necessary packages).
- Start the upstream services by running `/app/services/start.sh`.
- Start your service in the background or ensure it is running when you finish.
- The train/test split must not shuffle the joined data before splitting, or if it does, you must sort the joined data by `user_id` ascending before taking the first 80% as train and the remaining 20% as test, to ensure reproducibility. (Take the first 80% of rows after sorting by `user_id`).

Please create `/app/services/model_service.py` and run it so it listens on port 8080. Leave it running.