You are an AI assistant acting as a Machine Learning Engineer. Your objective is to build a reproducible machine learning pipeline that processes data using an embedded database, trains classification and regression models, and enforces strict numerical reproducibility.

You will start with a raw dataset generator script that you must create and run.
First, create a script `/home/user/generate_data.py` exactly as follows, and run it to generate the data:
```python
import pandas as pd
import numpy as np

np.random.seed(100)
n = 5000
df = pd.DataFrame({
    'id': range(n),
    'f1': np.random.randn(n),
    'f2': np.random.randn(n) * 2 + 1,
    'f3': np.random.rand(n),
    'f4': np.random.randn(n) - 1,
    'f5': np.random.randint(0, 10, n),
    'is_high_value': np.random.randint(0, 2, n),
    'score': np.random.randn(n) * 10 + 50
})
df.iloc[:4000].to_csv('/home/user/train.csv', index=False)
df.iloc[4000:].to_csv('/home/user/test.csv', index=False)
```

**Step 1: Environment Setup**
Install `pandas`, `scikit-learn`, and `duckdb`.

**Step 2: Data Storage Management**
Write a Python script `/home/user/ingest.py` that:
1. Creates a local DuckDB database at `/home/user/ml_data.duckdb`.
2. Reads `/home/user/train.csv` and `/home/user/test.csv` and loads them into DuckDB tables named `train_data` and `test_data` respectively.

**Step 3: Model Training and Prediction**
Write a Python script `/home/user/pipeline.py` that:
1. Connects to `/home/user/ml_data.duckdb` and extracts the training and testing tables into Pandas DataFrames.
2. Uses features `f1, f2, f3, f4, f5`.
3. Trains a `sklearn.linear_model.LogisticRegression` model to predict `is_high_value` (binary classification). Use `random_state=42`.
4. Trains a `sklearn.linear_model.Ridge` model (with `alpha=1.0`) to predict `score` (regression). Use `random_state=42`.
5. Computes predictions on `test_data`.
6. Calculates the training accuracy for the classifier and training Mean Squared Error (MSE) for the regressor.
7. Saves these metrics to `/home/user/metrics.json` in the exact format: `{"classification_accuracy": <float>, "regression_mse": <float>}`.
8. Saves the test predictions to `/home/user/predictions.csv` with columns: `id`, `class_pred`, `score_pred`.

**Step 4: Pipeline Reproducibility Testing**
Write a Bash script `/home/user/test_repro.sh` that:
1. Runs `/home/user/pipeline.py`.
2. Computes the MD5 checksum of `/home/user/predictions.csv` and saves it.
3. Runs `/home/user/pipeline.py` a second time.
4. Computes the MD5 checksum of `/home/user/predictions.csv` again.
5. If the checksums match perfectly (indicating numerical reproducibility), it writes the word `REPRODUCIBLE` to `/home/user/repro_status.txt`. If they do not match, it writes `FLAKY`.

Execute all necessary scripts (`generate_data.py`, `ingest.py`, `pipeline.py`, and `test_repro.sh`) to leave the system in the final state where all output files (`ml_data.duckdb`, `metrics.json`, `predictions.csv`, and `repro_status.txt`) exist and contain the correct values.