You are a machine learning engineer working on a recommendation system. A colleague has written a script to prepare data and generate baseline recommendations, but it contains critical data leakage flaws. The script applies imputation, outlier handling, and dimensionality reduction to the *entire* dataset before splitting it into training and test sets.

Your task is to fix the data leakage and correctly execute the pipeline.

**Initial Setup:**
You will find a script at `/home/user/leaky_pipeline.py` and a dataset at `/home/user/data.csv`.
The dataset contains 1000 rows. The first 800 rows represent the training set, and the last 200 rows represent the test set.

**Instructions:**
1. Fix the Python script `/home/user/leaky_pipeline.py`. You must rewrite the data processing steps so that there is absolutely no data leakage:
   - Split the dataset into train (first 800 rows) and test (last 200 rows) *before* any transformations.
   - **Missing Values:** Impute missing values using the median of the *training* set. Apply this fitted imputer to both train and test sets.
   - **Outliers:** Calculate the 1st and 99th percentiles for each feature on the *training* set. Clip the feature values in both train and test sets to these thresholds.
   - **Dimensionality Reduction:** Apply PCA to reduce the features to 10 components. Ensure PCA is initialized with `random_state=42`. Fit the PCA *only* on the training set, and transform both train and test sets.
   - **Recommendation:** Use a k-Nearest Neighbors classifier (`KNeighborsClassifier` from scikit-learn) with `n_neighbors=5` and `metric='euclidean'` to predict the `target_item` for the test set based on the transformed features. 

2. The Python script must save the final predictions to `/home/user/recommendations.csv` with exactly two columns: `user_id` and `recommended_item`.

3. **Execution Environment:** Numerical libraries often use multiple threads which can sometimes cause non-deterministic behavior. Create a bash script at `/home/user/run.sh` that sets the environment variables `OMP_NUM_THREADS=1`, `OPENBLAS_NUM_THREADS=1`, and `MKL_NUM_THREADS=1`, and then executes your fixed Python script.

Make sure your `run.sh` script is executable and run it to produce the final `recommendations.csv`.