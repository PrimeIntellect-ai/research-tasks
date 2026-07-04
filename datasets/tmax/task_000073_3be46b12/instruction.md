You are a data scientist tasked with cleaning a dataset of user embeddings. The dataset contains high-dimensional representations of users, but a bug in the pipeline created near-duplicate entries that need to be identified and removed.

The dataset is located at `/home/user/data/embeddings.csv`. It has a header row, an `id` column (integer), and 50 continuous feature columns named `v0` through `v49`.

Please perform the following data cleaning steps using Python:

1. **Dimensionality Reduction**: Apply Principal Component Analysis (PCA) to the 50 feature columns (do not scale the features beforehand). Determine the minimum number of principal components required to explain at least 90.0% (0.90) of the total variance. 
   - Write this exact integer to a file named `/home/user/pca_components.txt`.

2. **Similarity Search**: Transform the features into this reduced PCA space. In this reduced space, compute the Euclidean distance between all pairs of users. Find all pairs of users whose distance is strictly less than `0.25`.

3. **Deduplication**: Treat these close pairs as an undirected graph where edges connect near-duplicates. For every connected component in this graph, keep the user with the lowest `id` and mark all other users in that component for removal.
   - Write the `id`s of all users marked for removal to `/home/user/removed_ids.txt`, with one integer `id` per line, sorted in ascending order.

4. **Cleaned Dataset**: Output the original data (with all 50 original features, `v0` to `v49`, and `id`), excluding the removed users, to `/home/user/cleaned_embeddings.csv`. The rows should be sorted by `id` in ascending order. Include the header.

Ensure all output files are placed exactly as specified. You may install any standard Python data science libraries (e.g., `scikit-learn`, `numpy`, `pandas`) as needed.