You are an MLOps engineer investigating an experiment artifact that exhibits suspiciously high performance. You suspect a data leak in the training pipeline.

Your workspace contains the following raw data files:
- `/home/user/data/features.csv`: Contains feature data with an `id` column.
- `/home/user/data/labels.json`: Contains JSON array of objects with `id` and `target` keys.

There is also a training script at `/home/user/train.py` that currently performs data joining, preprocessing, and training. 

However, `train.py` contains a classic data leakage error: it applies `StandardScaler().fit_transform()` to the *entire* dataset before performing `train_test_split`. This leaks information from the test set into the training process.

Your task:
1. Review `/home/user/train.py` to understand the current logic and observe the data leak.
2. Create a fixed version of the script named `/home/user/train_fixed.py`.
3. The fixed script must:
    - Join `features.csv` and `labels.json` on `id`.
    - Perform `train_test_split` with `test_size=0.3` and `random_state=42`.
    - Apply `StandardScaler` correctly (fit on training data, transform training data, and transform test data using the fitted scaler).
    - Train a `LogisticRegression(random_state=42)` model.
    - Evaluate accuracy on the test set.
    - Save the trained model pipeline (Scaler + LogisticRegression) to `/home/user/model_fixed.pkl`.
4. Run both the leaky and fixed scripts to compare their results.
5. Create a report file at `/home/user/report.json` containing the exact test accuracies from both scripts. The JSON must have exactly this format:
```json
{
  "leaky_accuracy": <float>,
  "fixed_accuracy": <float>
}
```
Round the floats to 4 decimal places.

Ensure you install any necessary Python packages (like `pandas`, `scikit-learn`) to run the scripts.