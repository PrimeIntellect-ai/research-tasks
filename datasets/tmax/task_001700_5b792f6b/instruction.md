You are an ML Engineer preparing training data and building a baseline similarity index for a recommendation system. You need to clean a dataset of item embeddings, perform bootstrap sampling to simulate a larger dataset, and use a fast similarity search library to find nearest neighbors.

The environment is strictly offline. You have a vendored copy of the `annoy` library at `/app/annoy-1.17.3`. However, a colleague accidentally broke its configuration, and it fails to install. 

Follow these steps exactly:

1. **Fix and Install the Vendored Library**
   - Navigate to `/app/annoy-1.17.3`. Identify and fix the bug preventing its installation (hint: look at the source file names referenced in `setup.py`).
   - Install the package in your environment (e.g., `pip install .`).

2. **Clean the Data**
   - Load the raw item embeddings from `/home/user/embeddings.csv`. This file contains 1000 rows and 50 columns (no header).
   - **Missing Values:** Impute any `NaN` values using the *mean of that specific column*.
   - **Outliers:** Clip all numerical values in the dataset to be strictly within the range `[-2.0, 2.0]`.

3. **Bootstrap Sampling**
   - To test the robustness of the similarity search, create a bootstrapped dataset of exactly 5,000 items. 
   - Sample rows from the cleaned dataset *with replacement*. 
   - To ensure reproducibility, set your numpy random seed to `42` immediately before generating the random indices (e.g., `np.random.seed(42); indices = np.random.choice(...)`).
   - Save this bootstrapped dataset to `/home/user/bootstrapped_data.csv` (no header).

4. **Similarity Search and Recommendation**
   - Using the installed `annoy` package, build an index on your 5,000-item bootstrapped dataset. Use the `euclidean` distance metric and `n_trees=20`.
   - Take the **first 100 items** from your *original* 1000-item cleaned dataset.
   - For each of these 100 items, query the Annoy index to find its top 10 nearest neighbors within the 5,000-item bootstrapped dataset.
   - Save the results to `/home/user/neighbors.csv`. This file must have exactly 100 rows and 10 columns (comma-separated), where each value is the integer index (0-4999) of a nearest neighbor in the bootstrapped data.

Ensure all output files are placed in `/home/user/` with the exact names requested.