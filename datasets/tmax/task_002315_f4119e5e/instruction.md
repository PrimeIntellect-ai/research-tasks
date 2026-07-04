You are an MLOps engineer analyzing tracking artifacts from a large batch of machine learning experiments. The experiment metadata and early training metrics are scattered across different files, and you need to combine them, extract features, and build a predictive model to forecast the final validation accuracy of ongoing experiments.

Your workspace contains the following data at `/home/user/data/`:
1. `train_metadata.csv` and `test_metadata.csv`: Contains `exp_id`, `dataset_size`, `batch_size`, and `optimizer` (categorical: 'adam', 'sgd', 'rmsprop').
2. `metrics/`: A directory containing JSON files named `<exp_id>.json`. Each file contains `learning_rate`, `val_loss_curve` (a list of 10 floats representing the first 10 epochs), and for the training experiments, a `final_val_accuracy` float. (The test JSONs do NOT have `final_val_accuracy`).

Your task is to write a Python pipeline that accomplishes the following:

1. **Multi-source Data Joining:**
   Merge the CSV metadata with the JSON metrics for both the training and test sets using the `exp_id`.

2. **Dimensionality Reduction & Linear Algebra:**
   Extract the `val_loss_curve` for all experiments (train and test combined, shape $N \times 10$). Standardize this matrix so that each column (epoch) has zero mean and unit variance. 
   Using `sklearn.decomposition.PCA` (with `random_state=42`), reduce these standardized curves to exactly 2 principal components. These two components will serve as features representing the "shape" of the early learning curve.
   Compute the pairwise Cosine Similarity between the 2D PCA feature vectors of all experiments. Find the pair of experiments (e.g., "exp_012" and "exp_084") that have the highest cosine similarity.

3. **Feature Engineering & Modeling:**
   Prepare the feature matrix for modeling:
   - `dataset_size` (numeric)
   - `batch_size` (numeric)
   - `learning_rate` (numeric)
   - `optimizer` (one-hot encoded, drop the first category alphabetically to avoid collinearity)
   - `pca_component_1` (numeric)
   - `pca_component_2` (numeric)
   
   Using the training data, train a Ridge Regression model (`sklearn.linear_model.Ridge`) to predict the `final_val_accuracy`.
   Perform Cross-Validation and Hyperparameter Tuning using `GridSearchCV` with 5-fold cross-validation (`cv=5`) to find the best `alpha` among `[0.1, 1.0, 10.0, 100.0]`. Set `random_state=42` where applicable.

4. **Prediction and Reporting:**
   Use the best estimator from the grid search to predict the `final_val_accuracy` for the test experiments.
   
Output your final results into a JSON file at `/home/user/report.json` with the exact following structure:
```json
{
  "best_alpha": 1.0,
  "most_similar_pair": ["exp_012", "exp_084"],
  "test_predictions": {
    "exp_101": 0.8523,
    "exp_102": 0.9124
  }
}
```
*Note for `most_similar_pair`: Sort the two experiment IDs alphabetically. Do not compare an experiment with itself.*
*Note for `test_predictions`: Round the predictions to 4 decimal places.*