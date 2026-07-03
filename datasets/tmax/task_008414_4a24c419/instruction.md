As an MLOps engineer, we need to test the reproducibility and accuracy of our batch-processed dimensionality reduction pipeline against our exact baseline. We are simulating large-scale data storage using HDF5.

I have stored a dataset of feature vectors in an HDF5 file located at `/home/user/data/features.h5` under the dataset name `dataset`. 

Your task is to write a Python script at `/home/user/test_pca.py` that performs the following pipeline reproducibility test:
1. Load the dataset from `/home/user/data/features.h5` (read it entirely into memory for this test).
2. Fit a standard exact PCA model on the data using `sklearn.decomposition.PCA` with `n_components=10` and `svd_solver='full'`.
3. Fit an incremental PCA model on the same data using `sklearn.decomposition.IncrementalPCA` with `n_components=10` and `batch_size=100`. This simulates how we process out-of-core large-scale data.
4. Extract the `explained_variance_ratio_` array from both models.
5. Calculate the maximum absolute difference between the exact PCA's explained variance ratio and the Incremental PCA's explained variance ratio.
6. Save the results to `/home/user/report.json`. The JSON file must contain exactly one key `"max_diff"` mapping to the float value of the maximum absolute difference calculated in step 5.

Make sure your script executes successfully and generates the JSON file. You may need to install `h5py` and `scikit-learn` if they are not already present.