You are taking over a project from a junior machine learning engineer. They have built a custom modeling pipeline in `/home/user/ml_project/pipeline.py` that performs Principal Component Analysis (PCA) using `numpy` linear algebra operations, followed by a Linear Regression model. 

However, they reported suspiciously high performance. Upon review, you suspect they introduced a critical data leakage bug: they applied their custom PCA transformation (which computes the dataset mean and covariance matrix) to the entire dataset *before* splitting it into training and testing sets. This leaks information about the test set's distribution into the training phase.

Your task is to fix the pipeline:
1. Identify and fix the data leakage in `/home/user/ml_project/pipeline.py`. The data must be split into train and test sets (80/20 split, `random_state=42`, without shuffling) *before* any transformations are calculated.
2. The custom PCA function `custom_pca` uses `numpy.linalg.eigh`. You must keep this custom PCA implementation, but modify the pipeline so that the PCA parameters (mean and eigenvectors) are computed **strictly on the training data**.
3. Apply the computed PCA transformation to both the training and testing sets (using the training mean and training eigenvectors). Keep the number of components at 3.
4. Train the existing `LinearRegression` model on the correctly transformed training data and predict on the test data.
5. Track the experiment reproducibly by computing the Mean Squared Error (MSE) for both the train and test sets. Save these metrics to a file exactly at `/home/user/ml_project/metrics.json` with the following schema:
   ```json
   {
       "train_mse": <float rounded to 4 decimal places>,
       "test_mse": <float rounded to 4 decimal places>
   }
   ```

Do not use `sklearn.decomposition.PCA`; you must fix and use the `custom_pca` function provided in the script. Ensure all scripts are fully reproducible.

The dataset is located at `/home/user/ml_project/data.csv`. You can run and edit the code as much as you need to find and fix the issue.