You are an MLOps engineer investigating some experiment artifacts. A lightweight linear model was deployed, but its inference pipeline is broken. You need to manually process a small batch of validation data using the model's saved weights, handling data quality issues along the way.

You are provided with two files:
1. `/home/user/weights.csv`: A two-column CSV (with a header) containing the model's learned parameters. The columns are `feature` and `weight`. It contains weights for features `f1` and `f2`, as well as a `bias` term.
2. `/home/user/data.csv`: A tabular dataset (with a header) containing `id`, `f1`, and `f2`. 

Your task is to calculate the model's predictions for each row in `data.csv` applying the following preprocessing rules:
- **Missing Values:** If a feature value is completely missing (empty string), impute it with `0.0`.
- **Outliers:** Cap all feature values (after imputation) to the range `[-10.0, 10.0]`. Any value greater than `10.0` should become `10.0`, and any value less than `-10.0` should become `-10.0`.
- **Inference:** The model is a simple linear regression. The prediction is calculated as the dot product of the features and weights, plus the bias: `prediction = (f1 * weight_f1) + (f2 * weight_f2) + bias`.

Output Requirements:
Create a file at `/home/user/positive_predictions.csv`.
Write only the `id` and the calculated `prediction` for rows where the final `prediction > 0.0`.
The file should NOT have a header.
Format each row as `id,prediction` (e.g., `1,4.5`).
Ensure the rows are sorted in ascending order by `id`. You may write a script in any language or use shell utilities to complete this task.