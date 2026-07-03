You are an MLOps engineer tasked with tracking experiment artifacts and identifying potential methodological flaws in model training pipelines. 

A junior data scientist submitted a training script (`/home/user/train.py`) that models a continuous target from a dataset (`/home/user/data.csv`). However, you suspect there is a classic data leakage issue in their pipeline (specifically, applying a global transformation before the train/test split). You need to quantify the statistical impact of this bug.

Your task is to:
1. **Enforce Data Schema**: Read `/home/user/schema.json`. Ensure that you only use the columns defined in this schema for your modeling (drop any extra columns found in the CSV).
2. **Reconstruct the Leaky Pipeline**: Run or reproduce the logic in `/home/user/train.py` exactly as it is (scaling *before* splitting) to calculate the predictions of the Ridge model on the test set. Use the test set absolute errors.
3. **Build the Fixed Pipeline**: Create a corrected pipeline where the `StandardScaler` is fit **only** on the training data, and then used to transform both the train and test data. Train a new `Ridge(alpha=1.0)` model. 
    * *Note: For both pipelines, use `train_test_split` with `test_size=0.2` and `random_state=42`.*
4. **Hypothesis Testing**: Perform a two-sided paired t-test between the **absolute errors** of the leaky model's predictions and the fixed model's predictions on the test set.
5. **Reporting**: Generate a JSON file at `/home/user/report.json` with the following structure (do not round the numbers):
```json
{
  "leaky_mse": <float>,
  "fixed_mse": <float>,
  "p_value": <float>
}
```

Write whatever code or scripts you need to accomplish this. Save your final output strictly to `/home/user/report.json`.