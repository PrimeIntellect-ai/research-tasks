You are tasked with fixing a broken data pipeline, analyzing customer support logs, and building a predictive model.

**Step 1: Fix the Data Service**
In the `/app/` directory, there is a multi-service setup involving a Redis cache and a Flask API (`api.py`) that serves our raw CSV data. Currently, the API fails to start because of a misconfiguration in how it connects to Redis. 
1. Identify and fix the connection issue in `/app/api.py`.
2. Use the provided `/app/start_services.sh` to start Redis, the Flask API (runs on port 8000), and an MLflow tracking server (runs on port 5000). 
3. Verify it works by downloading the dataset via `curl http://localhost:8000/data.csv` and saving it to `/home/user/train.csv`.

**Step 2: Environment Setup**
Install necessary Python packages: `pandas`, `scikit-learn`, `mlflow`, `redis`, and `flask`.

**Step 3: Tokenization & Feature Engineering**
Write a Python script (`/home/user/train_model.py`) that reads `/home/user/train.csv`.
For the `customer_query` column, implement a custom tokenizer:
- Lowercase the text.
- Remove all characters except alphanumeric and spaces.
- Split by whitespace.
Compute the following features for each row:
- `num_tokens`: Total number of tokens.
- `num_unique`: Number of unique tokens.
- `char_per_token`: Average character length of tokens in the query (0 if no tokens).

**Step 4: Correlation and Tracking**
Compute the Pearson correlation matrix between your three engineered features and the `resolution_time` column.
Initialize an MLflow experiment named "Support_Analysis" (tracking URI: `http://localhost:5000`). Log the correlation values of the features against `resolution_time` as MLflow metrics.

**Step 5: Predictive Modeling**
Train a `Ridge` regression model (from `scikit-learn`, default parameters) using ONLY `num_tokens`, `num_unique`, and `char_per_token` to predict `resolution_time`. 
Save the trained model to `/home/user/model.pkl` using `joblib`.
Write an inference script `/home/user/predict.py` that takes a CSV file path as a command-line argument, applies the exact same tokenization and feature engineering, loads the model, and prints out the Mean Squared Error (MSE) rounded to 2 decimal places. 
Example usage: `python /home/user/predict.py /home/user/train.csv`

Ensure your model accurately captures the relationship to achieve an MSE below 50.0 on an unseen test set.