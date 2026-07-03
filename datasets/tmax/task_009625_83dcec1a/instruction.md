You are an AI assistant acting as a Data Engineer building a machine learning ETL pipeline. 

A synthetic dataset has been provided at `/home/user/dataset.csv`. It contains 10 continuous features (`f1` through `f10`) and a continuous target variable (`target`).

Your task is to write a Python script at `/home/user/pipeline.py` that processes the data and trains a model while strictly avoiding data leakage between the train and test sets.

The script must perform the following steps exactly:
1. Load `/home/user/dataset.csv`.
2. Split the data into training and testing sets (80% train, 20% test) using `sklearn.model_selection.train_test_split` with `random_state=42`. Do not shuffle manually before this step.
3. Perform feature selection using correlation analysis: compute the Pearson correlation coefficient between each feature and the `target`. To avoid data leakage, this correlation must be calculated **only on the training set**.
4. Select only the features that have an absolute correlation with the target of `>= 0.25`.
5. Scale the selected features using `sklearn.preprocessing.StandardScaler`. Again, ensure no data leakage occurs (the scaler must be fitted *only* on the training set).
6. Train a standard `sklearn.linear_model.LinearRegression` model using the scaled, selected training features.
7. Predict on the test set and calculate the Mean Squared Error (MSE).
8. Save the results to `/home/user/results.json` in the exact following format:
```json
{
  "selected_features": ["f1", "f2", ...],
  "test_mse": 1.2345
}
```
Round the `test_mse` to exactly 4 decimal places.

Make sure to install any required packages (like `pandas` and `scikit-learn`) before running your script.