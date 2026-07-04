You are a data engineer tasked with building an ETL and machine learning pipeline. 

We have a raw dataset located at `/home/user/raw_events.csv` (which is already present on the system). This dataset contains user event logs. One of the common pitfalls with this dataset is that pandas will silently convert integer columns to floats if there are missing values (NaNs). 

Your task is to write a Python script at `/home/user/pipeline.py` that performs the following steps:

1. **Install dependencies**: Ensure `pandas` and `scikit-learn` are installed (you can run pip commands in the terminal).
2. **Data Loading & Cleaning**: Load `/home/user/raw_events.csv`. The dataset has the following columns: `user_id`, `age`, `event_code`, `session_duration`, and `is_fraud` (target).
3. **Handle Missing Values & Types**: 
   - `session_duration` contains missing values. Impute them with the median `session_duration` of the training set (to avoid data leakage, calculate median only on the whole dataset for simplicity here, just use the column median).
   - `event_code` is meant to be an integer but has missing values. Impute missing `event_code` values with `-1`. Ensure that `event_code` is cast to an `int` so that no floats (like `1.0`) exist in this column.
4. **Feature Engineering**:
   - Create a new feature `is_youth` which is `1` if `age < 25`, else `0`.
   - One-hot encode the `event_code` column. The resulting columns should have integer suffix names (e.g., `event_code_-1`, `event_code_4`, etc. - ensure there are no `.0` decimals in the column names which happens if pandas treated it as float).
5. **Modeling**:
   - Define features (X): `age`, `session_duration`, `is_youth`, and all the one-hot encoded `event_code` columns.
   - Define target (y): `is_fraud`.
   - Split the data into training and testing sets using `train_test_split` with `test_size=0.25` and `random_state=42`.
   - Train a `LogisticRegression` model (with `random_state=42`, `max_iter=1000`) on the training set.
6. **Reporting**:
   - Predict on the test set.
   - Calculate the `accuracy` and `f1_score` (using `average='binary'`).
   - Save the processed complete dataframe (before splitting) to `/home/user/processed_events.csv` (do not include the index).
   - Save the metrics to a JSON file at `/home/user/metrics.json` with the exact keys: `"accuracy"` and `"f1_score"`.

Run your script to produce the final outputs.