You are an ML Engineer preparing training data. We have a high-dimensional dataset located at `/home/user/raw_data.csv` (without a header row). To optimize our downstream training pipeline, we need to apply dimensionality reduction, track the numerical accuracy of the compression, and store the output in an efficient large-scale data format.

Please write and run a Python script to perform the following:

1. Load the dataset from `/home/user/raw_data.csv`.
2. Use Principal Component Analysis (PCA) from `sklearn.decomposition` to reduce the dataset's dimensionality. Find the exact minimum number of principal components required such that the cumulative explained variance ratio is strictly greater than or equal to `0.95`.
3. Transform the raw data using this optimal number of components.
4. Save the transformed (reduced) data into an HDF5 file located at `/home/user/reduced_features.h5` under the dataset name `features`.
5. To test the numerical accuracy of this reduction, reconstruct the original dataset from the reduced features using the PCA inverse transform. Calculate the maximum absolute error (Max Absolute Error) between the original raw data and the reconstructed data across all elements.
6. Track your experiment by writing a JSON file to `/home/user/experiment_log.json` containing exactly two keys:
   - `"optimal_components"`: the integer number of components selected.
   - `"reconstruction_max_error"`: the calculated maximum absolute error as a float.

Ensure all file paths are strictly respected.