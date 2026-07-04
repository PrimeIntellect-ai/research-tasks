I am a researcher trying to organize my datasets and re-establish some baseline models for my experiments, but I lost the original Python modeling script. I only remember the model architecture and the hyperparameters we tested.

Please help me reconstruct the model, run the cross-validation hyperparameter sweep to track the experiments, and generate inference predictions on the test set.

Here are the details of the modeling pipeline:
1. **Model Architecture:** A standard machine learning pipeline consisting of `PolynomialFeatures` followed by a `Ridge` regression model (from `scikit-learn`).
2. **Hyperparameter Grid:**
   - Polynomial Degree: `[1, 2, 3, 4]`
   - Ridge Alpha: `[0.1, 1.0, 10.0]`
3. **Cross-Validation:** Use `KFold` with `n_splits=5`, `shuffle=True`, and `random_state=42`. 
4. **Metric:** Mean Squared Error (MSE).
5. **Data:** 
   - Training data: `/home/user/data/train.csv` (Contains columns `x` and `y`)
   - Test data: `/home/user/data/test.csv` (Contains column `x`)

Please do the following:
1. Reconstruct this exact pipeline in Python.
2. Evaluate all combinations of the hyperparameters using the specified cross-validation on the training data.
3. Track the experiment by saving the results to `/home/user/experiments/cv_results.csv`. This file must have a header `degree,alpha,mean_mse` and contain the 12 rows of hyperparameters and their corresponding Mean CV MSE. Round the `mean_mse` to exactly 4 decimal places. Sort the CSV by `mean_mse` in ascending order (best model first).
4. Identify the best hyperparameter combination (lowest mean MSE).
5. Retrain the pipeline with the best hyperparameters on the *entire* training dataset (`train.csv`).
6. Run inference on the test dataset (`test.csv`) using the retrained model.
7. Save the predictions to `/home/user/experiments/predictions.txt` (one prediction per line, formatted to 4 decimal places).

Create any missing directories if necessary. You will likely need to install `pandas` and `scikit-learn`.