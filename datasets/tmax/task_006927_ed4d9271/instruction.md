You are an AI assistant helping a data scientist set up a reproducible data cleaning and recommendation pipeline. 

We have a raw dataset of user-item ratings located at `/home/user/raw_ratings.csv`. The dataset has three columns: `user_id`, `item_id`, and `rating`. It contains some missing values and sparse users.

Your task is to write a Python script `/home/user/pipeline.py` that performs the following steps:

1. **Numerical Library Configuration**: Ensure that your script runs with OpenMP threads limited to 1 for reproducibility. You must enforce this by setting `OMP_NUM_THREADS=1` in the environment before executing the main Python logic.
2. **Data Cleaning**: Load the CSV using pandas. 
   - Drop any rows that contain missing (NaN) values.
   - Filter the dataset to retain ONLY users who have rated at least 3 items.
3. **Similarity Search Setup**: 
   - Pivot the cleaned dataset into a user-item matrix (rows = `user_id`, columns = `item_id`, values = `rating`). 
   - Fill any remaining missing values in the matrix with `0.0`.
4. **Cross-Validation and Hyperparameter Tuning**:
   - We want to find the best `k` for a k-Nearest Neighbors similarity search among users.
   - Using `sklearn.neighbors.NearestNeighbors(metric='cosine')`, evaluate `n_neighbors` in `[2, 3, 4]`.
   - Use `sklearn.model_selection.KFold` with `n_splits=3`, `shuffle=True`, and `random_state=42` to split the user-item matrix rows.
   - For each `k` and each fold: fit the NearestNeighbors model on the training set, and for the validation set, find the `k` nearest neighbors in the training set. Calculate the mean distance of these neighbors for the validation set.
   - Compute the overall mean distance across all 3 folds for each `k`.
5. **Experiment Tracking**:
   - Identify the `k` that yields the **lowest** overall mean distance.
   - Save the results to `/home/user/experiment_results.json` in the following format:
     ```json
     {
       "best_k": 2,
       "best_mean_distance": 0.1234
     }
     ```
   - Ensure the `best_mean_distance` is rounded to exactly 4 decimal places.

Run your script to generate the JSON file. Do not use external experiment tracking tools like MLflow; a simple JSON output is required for this automated environment.