You are a data scientist working for an agricultural tech company. You've received a batch of messy sensor data from smart greenhouses. Your task is to build a reproducible ETL and modeling pipeline that cleans this data, enforces a strict schema, and trains a baseline model to predict crop yield.

Here are the requirements for your task:

**1. Dependencies:**
Install any necessary Python packages (e.g., `pandas`, `scikit-learn`). 

**2. Data Cleaning and Schema Enforcement (ETL):**
The raw data is located at `/home/user/data/raw/messy_sensors.csv`. It contains the following columns: `sensor_id`, `temperature`, `humidity`, `soil_moisture`, and `yield_class`.
Write a Python script (`/home/user/pipeline.py`) that reads this data and applies the following schema and cleaning rules:
*   `sensor_id`: Must be a string starting with exactly "GH-". Drop rows that don't match.
*   `temperature`: Must be a numeric float. Drop rows with missing or unparseable values. Valid range is 10.0 to 40.0 (inclusive). Drop out-of-bounds rows.
*   `humidity`: Must be a numeric float. Drop rows with missing or unparseable values. Valid range is 20.0 to 90.0 (inclusive). Drop out-of-bounds rows.
*   `soil_moisture`: Must be a numeric float. Drop rows with missing or unparseable values. Valid range is 0.0 to 100.0 (inclusive). Drop out-of-bounds rows.
*   `yield_class`: Must be an integer (0, 1, or 2). Drop rows with missing or unparseable values, or values outside this set.

Save the cleaned dataset to `/home/user/data/clean/cleaned_data.csv` (keep the header).

**3. Model Training:**
In the same Python script, use the cleaned dataset to train a classification model:
*   Features (X): `temperature`, `humidity`, `soil_moisture`
*   Target (y): `yield_class`
*   Perform an 80/20 train-test split using `sklearn.model_selection.train_test_split` with `random_state=42`.
*   Train a `RandomForestClassifier` with `n_estimators=50` and `random_state=42`.
*   Evaluate the model's accuracy on the test set.
*   Save the trained model using `pickle` or `joblib` to `/home/user/model/rf_model.pkl`.
*   Save the test accuracy to `/home/user/report/metrics.json` in the following exact format: `{"accuracy": <float>}`.

**4. Reproducibility:**
Create a bash script at `/home/user/run_pipeline.sh` that makes the necessary directories (`/home/user/data/clean`, `/home/user/model`, `/home/user/report`) and then runs your `/home/user/pipeline.py` script. The bash script must be executable.

Ensure your pipeline runs entirely hands-off when `./run_pipeline.sh` is executed.