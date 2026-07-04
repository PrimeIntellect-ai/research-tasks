You are a Data Scientist tasked with cleaning a messy dataset and extracting its primary axis of variance.

The dataset is located at `/home/user/dataset.csv`. It contains three numerical columns: `X1`, `X2`, and `X3`. However, the data extraction pipeline has introduced some issues:
- Missing values are represented as the string `MISSING`.
- There are extreme outliers in some columns.
- Standard missing value handling in pandas can sometimes silently convert integers to floats. While the final output depends on the mathematical values, be mindful of your data types and cleaning steps.

Your task is to implement a robust data cleaning and analysis pipeline. You may write scripts in Python (or bash/R if you prefer) to perform the following steps:

1. **Impute Missing Values**: Replace any `MISSING` strings with the median of the available (non-missing) values in that specific column.
2. **Cap Outliers**: Use the Interquartile Range (IQR) method. For each column, calculate Q1 (25th percentile) and Q3 (75th percentile) using linear interpolation. Calculate `IQR = Q3 - Q1`. Cap any values below `Q1 - 1.5 * IQR` to `Q1 - 1.5 * IQR`, and any values above `Q3 + 1.5 * IQR` to `Q3 + 1.5 * IQR`.
3. **Compute Covariance**: Calculate the sample covariance matrix (using `N-1` degrees of freedom) of the cleaned, capped dataset.
4. **Extract Dominant Eigenvector**: Calculate the eigenvector corresponding to the largest eigenvalue of the covariance matrix. 
5. **Format Output**: Ensure the first element of the dominant eigenvector is positive (if it's negative, multiply the entire vector by -1). Round each component to exactly 4 decimal places.

Write the final 3 components of the dominant eigenvector as a comma-separated string (e.g., `0.1234,0.5678,0.8123`) to a file named `/home/user/eigenvector.txt`. 

No newline is required at the end of the file, but it's acceptable. The values must be exactly correct according to standard IEEE 754 floating point arithmetic operations.