You are a data scientist cleaning a high-dimensional dataset. You need to identify the optimal number of dimensions for downstream classification, and test the numerical accuracy of the dimensionality reduction to see how much information is lost.

A dataset has been provided at `/home/user/data.csv`. The target variable is named `target`, and all other columns (which start with `feat_`) are features.

Write a Python script at `/home/user/process.py` that performs the following steps:
1. Load `/home/user/data.csv`.
2. Construct a scikit-learn `Pipeline` containing a `PCA` transformer and a `RidgeClassifier(random_state=42)` estimator.
3. Use `GridSearchCV` with 5-fold cross validation (`cv=5`) to evaluate the pipeline on the dataset and find the best number of PCA components. Search over the following values for `pca__n_components`: `[5, 10, 15, 20]`.
4. Write the best number of components found by the grid search as an integer into a file at `/home/user/best_n.txt`.
5. Using a standalone `PCA` object initialized with this best number of components, fit the transformer on all the features and transform the data.
6. Reconstruct the original feature data by applying the `inverse_transform` method on the reduced data.
7. Compute the Mean Squared Error (MSE) across all elements between the original features and the reconstructed features.
8. Write this MSE value, rounded to exactly 4 decimal places, to a file at `/home/user/mse.txt`.

You may run the script yourself to ensure it produces the files.