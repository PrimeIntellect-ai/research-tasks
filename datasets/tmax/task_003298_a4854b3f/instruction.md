You are a Data Scientist tasked with cleaning a corrupted sensor dataset. The dataset contains three features (`x1`, `x2`, `x3`) and a `target` variable representing a physical measurement that must always be zero or positive. 

Currently, the dataset in `/home/user/dataset.csv` has two major issues:
1. Some `target` values are missing (`NaN`).
2. Some `target` values (both originally and potentially after initial imputation) are negative, which are physically impossible anomalies.

You must perform a multi-phase data cleaning and modeling process:

**Phase 1: Architecture Reconstruction and Inference**
A previous data scientist trained a PyTorch model to predict the `target` variable, but only left the weights file at `/home/user/weights.pth` and an incomplete model script at `/home/user/model.py`.
* Inspect the shape of the weights to deduce the correct hidden layer sizes.
* Fix `model.py` so the `SimpleMLP` class accurately reflects the trained architecture.
* Write a script to load the weights into the model and predict the `target` values strictly for the rows where `target` is currently `NaN`. Replace the `NaN` values in your dataset with these predictions.

**Phase 2: Cross-validation and Regression for Anomalies**
Even after fixing the `NaN`s, you will find negative values in the `target` column. 
* Identify all rows where `target < 0`. Treat these as anomalies.
* Train a scikit-learn `Ridge` regression model to predict `target` using features `x1, x2, x3`. 
* **Crucial:** Train this model *only* on the clean, valid rows (where `target >= 0` after Phase 1).
* Use `GridSearchCV` with 5-fold cross-validation to tune the `alpha` hyperparameter. Search over the values `[0.1, 1.0, 10.0]`. Set `random_state=42` if applicable (Ridge itself is deterministic, but ensure reproducible CV if you shuffle).

**Phase 3: Validation and Output**
* Use your best Ridge model to predict and replace all the anomalous negative `target` values.
* Save the fully cleaned dataset (with no `NaN`s and no negative values) to `/home/user/cleaned_dataset.csv`. Maintain the original column order and index.
* Create a JSON summary file at `/home/user/summary.json` with the following precise keys:
  * `"best_alpha"`: (float) The best alpha from your GridSearchCV.
  * `"imputed_nan_count"`: (int) The exact number of `NaN` values you replaced in Phase 1.
  * `"replaced_anomaly_count"`: (int) The exact number of negative values you replaced in Phase 3.
  * `"final_target_mean"`: (float) The mean of the `target` column in `cleaned_dataset.csv`, rounded to exactly 4 decimal places.

You may need to install standard data science libraries (e.g., `torch`, `pandas`, `scikit-learn`) using `pip`.