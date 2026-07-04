You are an MLOps engineer cleaning up some orphaned experiment artifacts on a legacy server. You have found two files:
1. `/home/user/data.csv` - A dataset of 10-dimensional embeddings (no headers).
2. `/home/user/weights.csv` - An unlabelled weights matrix. 

From the experiment logs, you know this weights matrix was used as a single linear layer (without bias) to perform dimensionality reduction, projecting the 10-dimensional data down to 3 dimensions.

Your task is to reconstruct the model's inference and evaluate its reconstruction loss:
1. Load both CSV files.
2. Project the embeddings in `data.csv` into the 3-dimensional latent space using the matrix in `weights.csv`. 
3. Reconstruct the original data from the 3-dimensional latent space using the transpose of the weights matrix.
4. Calculate the Mean Squared Error (MSE) between the original data and the reconstructed data (average over all elements).
5. Save the MSE, rounded to exactly 4 decimal places, to a new file at `/home/user/reconstruction_mse.txt`.
6. Save the 3-dimensional projected coordinates of the **first 3 rows** of the data to `/home/user/projected_head.csv`. Format it as comma-separated values, with each number rounded to exactly 4 decimal places. Do not include headers.

You may use any language (Python, bash+awk, etc.) to accomplish this.