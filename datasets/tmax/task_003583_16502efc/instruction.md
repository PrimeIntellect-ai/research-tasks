A researcher in our lab was organizing a large dataset of concept embeddings. Unfortunately, a flawed pandas pipeline silently introduced NaNs into the dataset, which cast the exact integer concept IDs to floats and wiped out several of the embedding vectors. 

We need you to clean the dataset, recover the missing embeddings, and compute a summary metric.

Here is what you have:
1. `/home/user/corrupted_data.csv`: A CSV file containing the corrupted data. The `concept_id` column contains float values (like `1042.0`) and some `NaN`s. The remaining 128 columns (`dim_0` to `dim_127`) contain the embedding vectors, but rows with `NaN` concept IDs have lost their embeddings (they are all NaNs).
2. `/app/embedder_oracle`: A stripped, compiled binary that generates the ground-truth 128-D embedding for a given valid integer concept ID. You can execute it via the command line (e.g., `/app/embedder_oracle 1042`) and it will print the 128 comma-separated float values of the embedding.

Your task:
1. Load `/home/user/corrupted_data.csv`.
2. Clean the `concept_id` column: drop rows where `concept_id` is NaN, and convert the remaining valid float IDs back to exact integers.
3. For any row where the embedding columns (`dim_0` to `dim_127`) contain NaNs, use the `/app/embedder_oracle` binary with the cleaned integer `concept_id` to reconstruct the exact 128-D vector.
4. Once the full $N \times 128$ data matrix is perfectly reconstructed, perform dimensionality reduction using Principal Component Analysis (PCA) to reduce the data to exactly 2 dimensions. Use `sklearn.decomposition.PCA` with `n_components=2`, `svd_solver='full'`, and `random_state=42`.
5. Compute the centroid (mean across all samples) of the resulting 2D dataset.
6. Write the 2D centroid coordinates to `/home/user/centroid.txt` as two comma-separated floats (e.g., `0.1234, -0.5678`).

The automated test will evaluate the L2 distance between your centroid and the reference centroid.