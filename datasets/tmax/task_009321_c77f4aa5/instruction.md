You are a data engineer working on an ETL pipeline. An upstream process has generated a Parquet file containing high-dimensional sensor data, but the current analysis script is producing "blank" or meaningless principal components because the features are on vastly different scales (similar to how a misconfigured matplotlib backend produces blank plots). 

Your task is to write a Python script `/home/user/process_data.py` that processes this data correctly.

The input data is located at `/home/user/input_data.parquet`. It contains 50 continuous feature columns (`feat_0` through `feat_49`) and one categorical column (`category` with values 'X' and 'Y').

Your script must perform the following exact steps:
1. Load the Parquet file into a Pandas DataFrame.
2. Extract the 50 continuous features.
3. Standardize the features so that each feature has a mean of 0 and a standard deviation of 1 (use `sklearn.preprocessing.StandardScaler`).
4. Apply Principal Component Analysis (PCA) to reduce the dimensionality of the standardized features down to exactly 2 components (`pc1` and `pc2`). (Use `sklearn.decomposition.PCA`).
5. Perform a Welch's two-sample t-test (unequal variances) on the values of the first principal component (`pc1`) to check for a significant difference between rows where `category == 'X'` and rows where `category == 'Y'`.
6. Save the resulting PCA-transformed data to a new Parquet file at `/home/user/output_data.parquet`. The output DataFrame must contain exactly three columns: `category`, `pc1`, and `pc2` (in that order).
7. Save the p-value from the t-test to a text file at `/home/user/p_value.txt`. The p-value must be formatted to exactly 4 decimal places (e.g., `0.0123`).

Ensure your script handles the data transformation efficiently and produces the exact output files requested. You can use standard data science libraries (pandas, numpy, scipy, scikit-learn, pyarrow/fastparquet).