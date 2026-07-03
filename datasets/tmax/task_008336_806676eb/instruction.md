You are acting as a Data Scientist on our fraud detection team. A colleague has written a script to join multi-source CSV files, train a fraud detection model, and evaluate its performance. However, there are a few issues with the current workflow:

1. **Data Leakage**: The current script scales the features on the entire dataset before splitting it into train and test sets, which causes data leakage. 
2. **Evaluation**: We need a more robust evaluation of the test set using bootstrap methods.
3. **Storage**: The intermediate joined dataset is not being saved efficiently.

You are provided with a working directory at `/home/user/fraud_project/`. 
Inside, you'll find:
- `data/users.csv`
- `data/transactions.csv`
- `data/labels.csv`
- `train_model.py` (the initial flawed script)

Your tasks are:
1. **Fix Data Leakage**: Modify `train_model.py` to prevent data leakage. You must split the data into train and test sets *before* fitting the `StandardScaler`. Use a scikit-learn `Pipeline` or fit the scaler only on the training set and transform both. Maintain the `test_size=0.2` and `random_state=42` for the `train_test_split`.
2. **Efficient Storage**: After joining the three dataframes (users, aggregated transactions, and labels) and before the train/test split, save the resulting merged pandas DataFrame to a Parquet file at `/home/user/fraud_project/data_merged.parquet`.
3. **Bootstrap Evaluation**: Instead of calculating a single ROC-AUC score on the test set, implement a bootstrap evaluation on the test set predictions. 
   - After training the model, get the predicted probabilities on the test set.
   - Perform 1000 bootstrap resamples (sampling with replacement) of the test set actual labels and predictions. Use `np.random.seed(42)` right before your bootstrap loop, and use `np.random.choice(len(y_test), size=len(y_test), replace=True)` to generate the indices for each resample.
   - Calculate the ROC-AUC score for each resample.
   - Compute the mean, 2.5th percentile (lower bound), and 97.5th percentile (upper bound) of these 1000 ROC-AUC scores.
4. **Output Results**: Save these metrics as a JSON file at `/home/user/fraud_project/metrics.json` with the following exact keys: `roc_auc_mean`, `roc_auc_lower`, `roc_auc_upper`.

Ensure your script runs successfully and generates the required files.