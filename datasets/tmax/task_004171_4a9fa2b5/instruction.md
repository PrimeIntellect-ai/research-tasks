You are an ML Engineer working on preparing training data for a user recommendation system. You have been given an ETL pipeline script that joins user profiles with their item interactions and standardizes the numerical features. 

However, the current pipeline has a serious flaw: **data leakage**. The script inadvertently leaks information from the test set into the training set during the feature engineering phase.

Your task is to:
1. Identify the data leakage bug in `/home/user/prepare_data.py`.
2. Fix the script so that the data is split into train and test sets *before* fitting the `StandardScaler`. The scaler must be fitted **only** on the training data, and then used to transform both the training and test sets.
3. Keep the `random_state=42` and `test_size=0.2` exactly as they are in the `train_test_split`.
4. Round the scaled columns (`age` and `income`) to 4 decimal places before saving to ensure deterministic output.
5. Save the resulting corrected datasets to `/home/user/train_clean.csv` and `/home/user/test_clean.csv` (keeping `index=False`).

Run the fixed script to generate the output files.