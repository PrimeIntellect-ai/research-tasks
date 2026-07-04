You are helping clean up a machine learning pipeline written by a junior data scientist. The pipeline lives in `/home/user/src/train.py`. It joins user data with transaction data, performs some feature scaling, splits the dataset, and evaluates a Logistic Regression model for fraud detection.

However, there are two major problems:
1. **Data Schema Violations**: The raw data sometimes contains negative transaction amounts and missing values for age. The current script does not handle this, which has caused downstream issues.
2. **Data Leakage**: The junior data scientist reported unexpectedly high test accuracy. Upon initial inspection, it appears they are applying `StandardScaler` to the entire dataset *before* performing the `train_test_split`, leaking information from the test set into the training set.

Your task:
1. Modify `/home/user/src/train.py` to enforce a strict data schema **after merging but before splitting**: explicitly drop any rows where `age` is missing (`NaN`) or where `amount` is strictly less than `0`.
2. Fix the data leakage bug. Ensure that `StandardScaler` is **fitted only on the training data**, and then used to transform both the training and test sets.
3. Keep the random states exactly as they are (`random_state=42` for both `train_test_split` and `LogisticRegression`, `test_size=0.2`).
4. Run the fixed script. It should write the corrected test accuracy to `/home/user/metrics_fixed.json` in the exact following JSON format:
   `{"accuracy": <float_value>}`

Do not modify the file paths for the input data in the script. Just fix the schema enforcement, the scaling leak, and output the correct JSON file.