You are an MLOps engineer working on tracking experiment artifacts. A colleague tried to evaluate a custom dimensionality reduction pipeline but inadvertently introduced data leakage by scaling and applying Principal Component Analysis (PCA) to the entire dataset before performing the train-test split and cross-validation. 

Your task is to properly implement and evaluate this pipeline from scratch, ensuring strict isolation between cross-validation folds to prevent any data leakage.

Here are your instructions:
1. You have a dataset located at `/home/user/dataset.csv`. The last column is the target variable (`target`), and all other columns are features.
2. Choose your preferred programming language and setup your environment (install any necessary packages like `pandas`, `scikit-learn`, `numpy`, etc.).
3. Create a machine learning pipeline that consists of three steps:
    a. **Standardization:** Scale features to have zero mean and unit variance.
    b. **Custom PCA:** Reduce the dimensionality to exactly `3` components. **Constraint:** You must implement the PCA transformation yourself using core linear algebra operations (e.g., SVD or Eigenvalue decomposition). Do NOT use pre-packaged PCA classes like `sklearn.decomposition.PCA`. You must wrap your implementation in a way that allows it to be cleanly inserted into a pipeline (e.g., a custom Transformer) so that `fit` and `transform` logic are separated.
    c. **Ridge Regression:** Fit a Ridge regression model.
4. Perform Cross-Validation and Hyperparameter Tuning:
    - Tune the Ridge regression regularization parameter `alpha` over the values: `[0.1, 1.0, 10.0]`.
    - Use 5-fold cross validation. If using Python's scikit-learn, use `KFold(n_splits=5, shuffle=True, random_state=42)`.
    - **Crucial:** Ensure absolutely no data leakage occurs. The scaler and the custom PCA must be fitted *only* on the training folds of each split, and then used to transform both the training and validation folds.
    - Evaluate using Mean Squared Error (MSE).
5. Output the best hyperparameter and the corresponding mean cross-validated MSE to a JSON file at `/home/user/best_model.json`. The file must have exactly this structure:
```json
{
  "best_alpha": 1.0,
  "cv_mse": 12.3456
}
```
(Replace 1.0 and 12.3456 with your actual computed values. Ensure `cv_mse` is positive).