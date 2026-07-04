You are an ML Engineer preparing a robust training dataset from a limited set of noisy sensor readings. You need to write a Python script that uses bootstrapping to expand the dataset, applies linear algebra to perform Principal Component Analysis (PCA) from scratch (do not use scikit-learn), and selects the top features.

Here are your instructions:

1. You are provided with a small dataset at `/home/user/sensor_data.csv`.
2. Write a Python script at `/home/user/prepare_data.py` that does the following:
   a. Loads the CSV using `pandas`.
   b. Performs bootstrap sampling to expand the dataset to exactly 10,000 rows. Use `pandas.DataFrame.sample(n=10000, replace=True, random_state=42)`.
   c. Standardizes the bootstrapped data (subtract the mean and divide by the population standard deviation, i.e., `ddof=0`).
   d. Computes the covariance matrix of the standardized data (which is equivalent to the correlation matrix). Use `numpy.cov` with `rowvar=False` and `bias=True`.
   e. Calculates the eigenvalues and eigenvectors of the covariance matrix using `numpy.linalg.eigh`.
   f. Sorts the eigenvectors in descending order of their corresponding eigenvalues.
   g. Projects the standardized bootstrapped data onto the top 2 principal components (the 2 eigenvectors with the highest eigenvalues).
   h. Saves the resulting projected 10,000-row dataset to `/home/user/processed_features.csv`. The file should have a header row with column names `PC1` and `PC2` and the values should be rounded to exactly 4 decimal places.

3. Run your script to generate `/home/user/processed_features.csv`.

Note: You may need to install `pandas` and `numpy` using `pip`. Do NOT use `sklearn` or any other ML libraries; you must implement the PCA projection using `numpy` linear algebra functions.