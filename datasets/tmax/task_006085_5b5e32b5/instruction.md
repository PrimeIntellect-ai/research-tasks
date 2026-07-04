You are a data scientist analyzing multi-dimensional sensor readings from a chemical reactor. The data has been logged in a messy, unstructured format and you need to perform dimensionality reduction to extract the primary signals.

Your task is to write and execute a Python script to process this data.

Here are the requirements:
1. Load the dataset located at `/home/user/sensor_data.csv`. The file is in a "long" format with columns: `time`, `sensor`, and `reading`.
2. Reshape the data into a "wide" format matrix where each row represents a unique `time` (sorted chronologically) and each column represents a `sensor` (sorted alphabetically). 
3. Mean-center the data (subtract the mean of each sensor column from the respective column).
4. Perform Singular Value Decomposition (SVD) on the mean-centered data matrix to factorize it into $U \Sigma V^T$. Use `numpy.linalg.svd` (or equivalent `scipy` function) with `full_matrices=False`.
5. Save the singular values (the diagonal elements of $\Sigma$) to a file named `/home/user/singular_values.txt`. Write one value per line, rounded to 4 decimal places.
6. Project the centered data onto the first two principal components (which correspond to the two largest singular values) to reduce it to 2 dimensions.
7. Create a scatter plot of this 2D projection (PC1 on the x-axis, PC2 on the y-axis) and save it to `/home/user/pca_plot.png`.

Your final output must include `/home/user/singular_values.txt` and `/home/user/pca_plot.png`.