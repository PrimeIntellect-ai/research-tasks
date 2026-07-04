You are a Machine Learning Engineer responsible for preparing a training pipeline for a new regression model. 

In our previous pipeline, we encountered a critical data corruption issue: when joining datasets, pandas silently converted integer identifiers and count features to floats due to the introduction of `NaN` values. This caused precision loss and downstream linear algebra routines to fail.

Your task is to build a robust, reproducible Python pipeline that cleans the data and trains a model, ensuring strict data type management and efficient storage.

Please execute the following steps:

1. **Environment Setup**
Install any necessary Python packages. You will likely need `pandas`, `scikit-learn`, and `pyarrow`.

2. **Data Preparation (`/home/user/project/prepare.py`)**
Write a Python script that reads `/home/user/project/raw_features.csv`.
The CSV has the following columns: `id`, `user_id`, `click_count`, `time_spent`, `target`.
- Some values in `user_id` and `click_count` are missing (empty strings/NaN).
- Impute all missing values in `user_id` and `click_count` with `-1`.
- **Critical:** Ensure `id`, `user_id`, and `click_count` are strictly cast to standard NumPy `int64` (do not use nullable `Int64` or `float64`).
- Standardize the `time_spent` column using `sklearn.preprocessing.StandardScaler` (fit and transform on the whole dataset).
- Save the processed dataframe to `/home/user/project/processed.parquet`. Use the `pyarrow` engine with `snappy` compression.

3. **Model Training (`/home/user/project/train.py`)**
Write a script that:
- Reads `/home/user/project/processed.parquet`.
- Uses `user_id`, `click_count`, and `time_spent` as features (X), and `target` as the target (y).
- Splits the data into training and testing sets: 80% train, 20% test. Use `sklearn.model_selection.train_test_split` with `random_state=42` and `shuffle=False`.
- Trains a `sklearn.linear_model.Ridge` model with `alpha=1.0` and `random_state=42` on the training set.
- Predicts on the test set and calculates the Mean Squared Error (MSE).
- Saves the MSE to a JSON file at `/home/user/project/metrics.json` in the exact format: `{"mse": <float_value>}`.

Ensure your scripts are executed and the final files (`processed.parquet` and `metrics.json`) are successfully generated.