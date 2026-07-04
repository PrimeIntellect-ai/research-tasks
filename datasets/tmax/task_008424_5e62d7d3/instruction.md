I am an MLOps engineer trying to track down a bug in an experiment. I have a model training script located at `/home/user/train.py` that processes a dataset (`/home/user/data.csv`), trains a Logistic Regression model, and outputs the test accuracy to `/home/user/metrics.json`. 

However, the reported accuracy is overly optimistic because of a classic data leakage issue: the `StandardScaler` is being fitted and applied to the entire dataset *before* the train-test split.

Your task is to:
1. Install the required Python packages (`pandas` and `scikit-learn`).
2. Fix the Python script `/home/user/train.py` so that the data leakage is resolved. Specifically, you must:
   - Split the raw data first using `train_test_split` with `test_size=0.2` and `random_state=42`.
   - Fit the `StandardScaler` **only** on the training data.
   - Transform both the training and test sets using this fitted scaler.
   - Train the `LogisticRegression` model (keep `random_state=42`) on the scaled training data.
   - Evaluate the model on the scaled test data and save the accuracy to `/home/user/metrics.json` exactly as the script originally did.
3. Modify the script to also save the properly scaled training features (`X_train_scaled`) to `/home/user/X_train_fixed.csv`. Use `numpy.savetxt` with `delimiter=','` to save it (no headers, no index).
4. Run the fixed script so that both `/home/user/metrics.json` and `/home/user/X_train_fixed.csv` are generated.

Do not alter the random seeds or the model hyperparameters.