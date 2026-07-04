You are an ML Engineer preparing training data and tracking experiments for a predictive maintenance project. 

Your goal is to build a data pipeline that joins multiple data sources, performs cross-validation with hyperparameter tuning, and tracks the experiments using an MLflow tracking server.

Here are the step-by-step requirements:

1. **Environment Setup:**
   - Install `pandas`, `scikit-learn`, and `mlflow` using pip.
   - Start a local MLflow tracking server running on `http://127.0.0.1:5000` in the background. Ensure the server is up and running before your script interacts with it.

2. **Data Processing:**
   - You have two datasets located in `/home/user/data/`:
     - `/home/user/data/sensors.csv`: Contains `timestamp`, `machine_id`, `temperature`, and `vibration`.
     - `/home/user/data/labels.json`: A JSON array of objects containing `timestamp`, `machine_id`, and `wear_level`.
   - Write a Python script that joins these two datasets perfectly on `machine_id` and `timestamp`. 

3. **Modeling & Cross-Validation:**
   - Features: `temperature`, `vibration`.
   - Target: `wear_level`.
   - Use `GroupKFold` with `n_splits=3`, grouping the splits by `machine_id` (so that data from the same machine does not appear in both train and validation sets for a given fold).
   - The model to evaluate is `sklearn.linear_model.Ridge`.

4. **Experiment Tracking & Tuning:**
   - Set up your script to track experiments via your local MLflow server.
   - Set the MLflow experiment name to `"Wear_Prediction"`.
   - Perform a grid search over the following `alpha` values for the Ridge model: `[0.1, 1.0, 10.0]`.
   - For each `alpha`, compute the mean cross-validated R-squared ($R^2$) score across the 3 folds.
   - Log the `alpha` parameter and the corresponding mean `cv_r2` metric to MLflow for each run.

5. **Reporting:**
   - After the tuning sweep is complete, programmatically determine the `alpha` that yielded the highest mean CV $R^2$ score.
   - Write a JSON file to `/home/user/best_run.json` with the exact keys `"best_alpha"` and `"best_cv_r2"`. Format the values as a float.
   - The values should be rounded to 4 decimal places.

Ensure the final JSON file is created and the MLflow server has the recorded runs before completing the task.