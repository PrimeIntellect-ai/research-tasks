You are a data engineer tasked with building a reproducible machine learning ETL and training pipeline for predictive maintenance. 

We have a raw dataset located at `/home/user/raw_data.csv` (which contains synthetic sensor data). The dataset has the following columns:
- `sensor_id` (integer)
- `temperature` (float, has missing values)
- `vibration` (float, has missing values)
- `pressure` (float)
- `status` (integer: 0 or 1, representing failure status)
- `remaining_life` (float, remaining useful life in hours)

Your objective is to build a pipeline consisting of data processing, model training (both classification and regression), and experiment tracking.

Step 1: Write an ETL script (`/home/user/etl.py`)
This script must read `/home/user/raw_data.csv` and perform the following preprocessing steps exactly:
1. Drop any rows where `temperature` is missing (NaN).
2. For missing `vibration` values, fill them with the median `vibration` of the entire dataset (after dropping missing temperatures).
3. Apply standard scaling (mean=0, variance=1) to `temperature`, `vibration`, and `pressure`. Use `sklearn.preprocessing.StandardScaler`.
4. Save the resulting processed DataFrame to `/home/user/processed_data.csv`. The output CSV must include the scaled feature columns, as well as `sensor_id`, `status`, and `remaining_life`. Do not write the index.

Step 2: Write a training script (`/home/user/train.py`)
This script must read `/home/user/processed_data.csv` and perform two tasks using the features `temperature`, `vibration`, and `pressure`:
1. **Classification**: Predict `status`.
   - Perform an 80/20 train-test split using `sklearn.model_selection.train_test_split` with `random_state=42`.
   - Train a `LogisticRegression` model with `random_state=42` and default parameters on the training set.
   - Calculate the Accuracy on the test set.
2. **Regression**: Predict `remaining_life`.
   - Perform an 80/20 train-test split using `sklearn.model_selection.train_test_split` with `random_state=42`.
   - Train a `Ridge` regression model with `alpha=1.0` and `random_state=42` on the training set.
   - Calculate the Mean Squared Error (MSE) on the test set.

Step 3: Experiment Tracking
Modify `train.py` so that after evaluating both models, it appends exactly two JSON lines (JSONL format) to `/home/user/experiments.jsonl`. Each line must be a valid JSON object with the following keys:
- `"model_type"`: (string) either `"LogisticRegression"` or `"Ridge"`
- `"target"`: (string) either `"status"` or `"remaining_life"`
- `"metric_name"`: (string) either `"accuracy"` or `"mse"`
- `"metric_value"`: (float) the calculated metric rounded to 4 decimal places.

Step 4: Reproducible Pipeline
Create a `Makefile` in `/home/user/` with the following targets:
- `etl`: Runs `etl.py`
- `train`: Runs `train.py`
- `all`: Runs `etl` then `train`

To complete the task, build the scripts and run `make all`. Ensure `/home/user/experiments.jsonl` contains the correct JSONL outputs.