You are a Data Engineer building a machine learning ETL pipeline. We need to process incoming batches of data, validate them against a strict schema, run them through a classification model, and save the results.

Your task is to write and execute a Python script that does the following:

1. **Train a Model**:
   - Read the training dataset from `/home/user/train.parquet`.
   - Train a standard `LogisticRegression` model from `scikit-learn` using default parameters (except set `random_state=42`).
   - The features are `f1`, `f2`, and `f3`. The target column is `label`.

2. **Schema Enforcement (Data Validation)**:
   - Read the new batch of data from `/home/user/incoming.parquet`.
   - Enforce the following schema rules. You must **drop** any rows that violate these rules:
     - `f1`: must be a float greater than 0.
     - `f2`: must be a float (no value constraints).
     - `f3`: must be a float less than 100.
   - The `incoming.parquet` dataset has an `id` column. Preserve it.

3. **Inference and Output Validation**:
   - Use the trained model to predict the class label (`predicted_label`) and the probability of the positive class (`probability` - class 1) for the valid rows.
   - Ensure the `probability` is strictly between 0.0 and 1.0 (inclusive). If any row has a probability outside this range, drop it (though Logistic Regression shouldn't produce this, add the check for output validation).

4. **Save Data**:
   - Save the fully processed and predicted dataset to `/home/user/processed_data.parquet`.
   - The final file must contain exactly these columns: `id`, `f1`, `f2`, `f3`, `predicted_label`, `probability`.

You will need to install any required Python packages (like `pandas`, `pyarrow`, `scikit-learn`) yourself.