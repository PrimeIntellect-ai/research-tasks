You are tasked with fixing a broken data processing pipeline, integrating dimensionality reduction, and setting up experiment tracking. 

You have been provided with two datasets in `/home/user/data/`:
1. `users.csv`: Contains `user_id`, `age`, and `target` (0 or 1).
2. `transactions.csv`: Contains `user_id`, `amount`, and `group_id` (an integer code). 
*Note: Not all users have transactions.*

Currently, when these tables are joined (left join on `user_id`), pandas silently converts the `group_id` column from integers to floats due to the introduction of `NaN` values for users without transactions. 

Your objective is to build a complete reproducible pipeline by writing a Python script `/home/user/pipeline.py` that does the following:

1. **Data Cleaning & Feature Engineering**: 
   - Load and left-join `users.csv` and `transactions.csv` on `user_id`.
   - Fix the silent int-to-float upcasting issue: impute missing `amount` values with `0.0` and missing `group_id` values with `0`. Ensure `group_id` is represented as an integer dtype.
   - Create a new feature `group_hash` by applying a bitwise left shift by 1 to `group_id` (i.e., `group_id << 1`). This operation will fail if `group_id` contains floats or NaNs.
   - Save the cleaned and engineered dataframe to `/home/user/cleaned_data.csv`.

2. **Dimensionality Reduction & Modeling**:
   - Extract features `age`, `amount`, and `group_hash`.
   - Use `sklearn.decomposition.PCA` to reduce these 3 features down to 2 components.
   - Split the data into train and test sets (80/20 split, `random_state=42`).
   - Train a `RandomForestClassifier(random_state=42)` on the PCA components to predict the `target`.

3. **Experiment Tracking**:
   - Install `mlflow` and `scikit-learn`.
   - Start a local MLflow tracking server running on `http://127.0.0.1:5000` in the background.
   - In your `pipeline.py`, connect to this local MLflow server.
   - Set the MLflow experiment name to `Data_Cleaning_Exp`.
   - Log the parameter `n_components` (value: 2).
   - Log the metric `accuracy` (the accuracy score of your model on the test set).

Run your pipeline script successfully. Leave the MLflow server running in the background when you are finished.