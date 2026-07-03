You have been given a machine learning evaluation script at `/home/user/evaluate_model.py` and a dataset at `/home/user/data.csv`. 

Currently, the script calculates the Mean Squared Error (MSE) of a Ridge regression model. However, the original author made a critical mistake: there is data leakage occurring during the data preprocessing phase (the features are scaled before the train/test split, meaning information from the test set leaks into the training process).

Your task is to:
1. Identify and fix the data leakage in `/home/user/evaluate_model.py`. 
2. You must apply the scaling correctly (fit on training data, transform on test data) using `StandardScaler` or an `sklearn.pipeline.Pipeline`.
3. Do not change the `test_size=0.2`, `random_state=42` (for both splitting and the model), or the model parameters (`Ridge(alpha=1.0)`).
4. Run your fixed pipeline to compute the accurate Test MSE.
5. Save the corrected Test MSE (rounded to exactly 4 decimal places) to a file named `/home/user/fixed_mse.txt`.
6. Save the first 10 predictions on the test set from your fixed model to a text file `/home/user/predictions.txt`, one prediction per line, rounded to 4 decimal places.

Ensure you do not alter the dataset itself, only the Python script.