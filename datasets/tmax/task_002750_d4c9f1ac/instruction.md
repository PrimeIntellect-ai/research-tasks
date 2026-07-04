You are tasked with fixing a machine learning script that has a critical data leakage issue, and then implementing a reproducible tracking pipeline. 

In `/home/user/data_project`, you will find a Python script named `train_model.py` and a script `generate_data.py`. 
First, run `python /home/user/data_project/generate_data.py` to create the working dataset `dataset.csv`.

The current `train_model.py` script applies standard scaling and Principal Component Analysis (PCA) for dimensionality reduction to the *entire* dataset before splitting it into train and test sets. This causes data leakage, as information from the test set influences the scaling and PCA components.

Your task:
1. Refactor `train_model.py` to prevent this data leak. You must use `sklearn.pipeline.Pipeline` to chain the `StandardScaler`, `PCA`, and `LogisticRegression` steps.
2. The dataset must be split into training and testing sets *before* any transformations are applied. Use `test_size=0.2` and `random_state=42` in `train_test_split`.
3. Keep the model as `LogisticRegression` with `random_state=42`. Keep PCA components at `10` with `random_state=42`.
4. Implement basic experiment tracking: calculate the test accuracy, and extract the explained variance ratio of the *first* PCA component from the fitted pipeline.
5. Save these metrics to a JSON file at `/home/user/data_project/metrics.json` with the exact keys `"test_accuracy"` and `"pca_explained_variance_1"`.
6. Serialize the fitted pipeline object to `/home/user/data_project/model.pkl` using `joblib`.

Ensure all code runs successfully and output files are created in the exact requested locations.