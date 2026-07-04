You are an MLOps engineer evaluating different model artifacts to deploy. You need to identify the best model based on a specific evaluation slice and a complexity penalty. 

You have the following files on your system:
- `/home/user/data/eval.csv`: The ground truth dataset. It contains columns `id`, `f1`, and `y_true`.
- `/home/user/artifacts/`: A directory containing multiple prediction files named `preds_<model_id>.csv`. Each file has columns `id` and `y_pred`.
- `/home/user/artifacts/metadata.json`: A JSON file containing metadata for each model. The format is `{"<model_id>": {"num_features": <integer>}}`.

Write a Python script to perform the following evaluation pipeline:
1. Load the evaluation dataset.
2. Engineer a new feature `f1_z` which is the z-score of the `f1` column. Calculate the z-score using the population standard deviation (i.e., `ddof=0` in numpy/pandas).
3. Filter the evaluation dataset to create an "evaluation slice". The slice should only contain rows where `f1_z > 0`.
4. For each model in the artifacts directory:
    - Load its predictions.
    - Match the predictions to the ground truth in the evaluation slice using the `id` column.
    - Calculate the Mean Squared Error (MSE) of the predictions on this specific evaluation slice.
    - Retrieve the `num_features` for the model from `metadata.json`.
    - Calculate the model's final penalized score using the formula: `penalized_score = MSE + (0.5 * num_features)`.
5. Identify the model with the lowest `penalized_score`.

Write the results to a file named `/home/user/best_model.txt`. The file must contain exactly one line in the following format:
`Model: <model_id>, Score: <score>`

Where `<score>` is rounded to exactly 4 decimal places (e.g., 2.7500).

Your task is to write the necessary code, run it, and ensure `/home/user/best_model.txt` is created with the correct answer.