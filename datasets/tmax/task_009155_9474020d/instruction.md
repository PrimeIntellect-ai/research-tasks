You are a data scientist tasked with cleaning a high-dimensional dataset that contains redundant information. We suspect that many of the features in the dataset are exact linear combinations of a smaller set of latent features.

Your objective is to determine the intrinsic dimensionality (rank) of the dataset and verify that the data can be perfectly reconstructed from this lower-dimensional space within standard numerical precision.

Please perform the following steps:
1. Install any necessary Python packages (e.g., `numpy`, `pandas`, `scikit-learn`).
2. Read the dataset located at `/home/user/dataset.csv`. The dataset has no header and contains floating-point numbers separated by commas.
3. Use linear algebra or dimensionality reduction techniques (e.g., SVD or PCA) to determine the exact mathematical rank of the dataset (the number of linearly independent components). Note that due to floating-point arithmetic, singular values won't be exactly zero, but there will be a significant drop-off.
4. Save the integer value of the rank to a file named `/home/user/rank.txt`.
5. Reconstruct the original dataset using ONLY the top `R` components, where `R` is the rank you determined.
6. Calculate the Mean Squared Error (MSE) between the original dataset and your reconstructed dataset to test numerical accuracy.
7. Save the MSE value (as a floating point number) to a file named `/home/user/mse.txt`.

Ensure your Python script handles the calculations accurately and efficiently.