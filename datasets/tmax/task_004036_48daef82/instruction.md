You are acting as a Machine Learning Engineer. I need you to clean a raw text dataset, identify anomalous examples using embeddings, and train a baseline classifier. 

Here are your instructions:

1. **Environment Setup**: 
   Create a Python virtual environment at `/home/user/venv` and install `scikit-learn` and `sentence-transformers`.

2. **Data Processing Script**:
   Create a Python script at `/home/user/pipeline.py` that performs the following steps:
   - Read the dataset from `/home/user/raw_data.jsonl`. Each line is a JSON object with keys: `id` (integer), `text` (string), and `label` (string).
   - Compute embeddings for all `text` fields using the `sentence-transformers` model `all-MiniLM-L6-v2`.
   - Identify anomalous records (outliers) in the embedding space using `sklearn.ensemble.IsolationForest`. Initialize it with `random_state=42` and `contamination=0.1`.
   - Filter out these outliers from the dataset.
   - Save the `id` of every outlier to `/home/user/outliers.txt`, with one integer ID per line, sorted in ascending order.

3. **Model Training & Evaluation**:
   - Using only the **inliers** (the non-anomalous records), split the data into training and testing sets using `sklearn.model_selection.train_test_split` with `test_size=0.2` and `random_state=42`. Use the embeddings as your features (X) and the `label` as your target (y).
   - Train a `sklearn.linear_model.LogisticRegression` classifier with `random_state=42` and `max_iter=1000` on the training set.
   - Evaluate the model on the test set and calculate the accuracy.
   - Write the accuracy to `/home/user/metrics.txt` in the exact format: `Accuracy: 0.XXXX` (rounded to 4 decimal places).

Execute your script to produce `/home/user/outliers.txt` and `/home/user/metrics.txt`.