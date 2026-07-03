You are a data engineer working on an ETL pipeline that processes text data, generates embeddings via TF-IDF, reduces dimensionality using PCA, and trains a simple Logistic Regression classifier. 

Your colleague wrote a draft pipeline script located at `/home/user/etl_pipeline.py` to process the dataset `/home/user/data.csv`. However, the model's performance on the test set is suspiciously high. We suspect there is a critical data leakage bug in how the transformations (TF-IDF and PCA) are being applied relative to the train/test split.

Your task:
1. Identify and fix the data leakage in `/home/user/etl_pipeline.py`. Ensure that any stateful transformations (like vectorizers, scalers, or dimensionality reduction models) are ONLY fitted on the training data, and then used to transform both the training and test data.
2. The split should use `test_size=0.3` and `random_state=42`.
3. The model should be `LogisticRegression(random_state=42)`.
4. Run the corrected pipeline.
5. Modify the script so that at the end of its execution, it saves a JSON file named `/home/user/metrics.json` containing the following keys:
   - `"test_accuracy"`: The accuracy score of the model on the test set (as a float).
   - `"first_5_predictions"`: A list of the first 5 predicted labels for the test set.

Make sure you do not change the random seeds provided in the original script so that the output is reproducible.