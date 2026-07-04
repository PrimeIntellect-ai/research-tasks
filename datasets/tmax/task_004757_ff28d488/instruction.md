You are a data researcher tasked with organizing and analyzing a corrupted dataset of sensor readings. Your goal is to write a Go program that cleans the data, performs covariance and correlation analysis, and extracts the primary dimensions of variance using Eigen decomposition (a fundamental step in Principal Component Analysis).

The dataset is located at `/home/user/data/sensor_data.csv`. It has a header row and four numerical feature columns (`F1`, `F2`, `F3`, `F4`). 
Due to a logging error, missing values were recorded as `-9999.0` or `-9999` (which in dynamic languages might silently convert to floats, but here needs explicit filtering).

Write a Go program at `/home/user/analyze.go` that does the following:
1. Initializes a Go module (`go mod init sensor_analysis`) and uses the `gonum.org/v1/gonum` library for numerical operations.
2. Reads the CSV and strictly filters out **any row** that contains `-9999` or `-9999.0` in any of its columns.
3. Using the cleaned dataset, calculates the Pearson correlation coefficient between `F1` and `F2`.
4. Computes the 4x4 covariance matrix of the cleaned dataset (across all 4 features).
5. Computes the eigenvalues of the covariance matrix to find the principal components of variance.
6. Writes the results to `/home/user/results.json` with the following exact JSON structure:
```json
{
  "clean_row_count": <integer>,
  "correlation_f1_f2": <float rounded to 4 decimal places>,
  "max_eigenvalue": <float rounded to 4 decimal places>
}
```

Constraints:
- You must use Go to perform this analysis.
- Output floats must be correctly rounded to exactly 4 decimal places.