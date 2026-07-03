You are a Data Scientist tasked with building an automated, reproducible data analysis service. An upstream bug recently corrupted our event pipeline, injecting `NaN` values into our strictly integer-based feature sets. Because of pandas' default behavior, this silently converted the integer columns into floats, which breaks our proprietary anomaly scoring engine.

You need to create a Python web service that cleans this data, queries an opaque, compiled scoring oracle, and performs statistical analysis.

**Requirements:**
1. **The Service:** Create a Python API (using Flask or FastAPI) listening on `127.0.0.1:8000`.
2. **The Endpoint:** Expose a `POST /api/analyze` endpoint that accepts `multipart/form-data` with a single file field named `file`. The uploaded file will be a CSV with a header row and 5 columns: `f1, f2, f3, f4, f5`.
3. **Data Cleaning Pipeline:**
   - Parse the CSV.
   - For any missing (`NaN`) values in a column, impute them using the median of that column (computed ignoring NaNs).
   - Round the imputed median to the nearest whole number (half to even) and cast all 5 columns back to standard integers (`int64`).
4. **Oracle Querying:** 
   - A proprietary scoring engine is located at `/app/prop_scorer`. It is a stripped binary.
   - The binary accepts the path to a headless, comma-separated CSV file of exactly 5 integer columns as its first CLI argument (e.g., `/app/prop_scorer /tmp/cleaned.csv`).
   - It outputs one float per line to `stdout`, representing the `prop_score` for each row.
5. **Statistical Analysis:**
   - **Correlation:** Calculate the Pearson correlation coefficient between the cleaned `f3` column and the returned `prop_score`.
   - **Dimensionality Reduction:** Standardize the 5 cleaned integer columns (subtract mean, divide by sample standard deviation, i.e., standard `StandardScaler`) and perform PCA to extract the first Principal Component (PC1).
   - **Hypothesis Testing:** Calculate the 95% confidence interval for the mean of PC1 using the normal approximation (i.e., $Z = 1.96$, formula: $\mu \pm 1.96 \times (\sigma / \sqrt{n})$). Note: since the data is standardized before PCA, the mean of PC1 should be very close to 0, but compute it exactly based on the sample.
6. **Response:** Return a JSON payload with exactly these keys, rounding all values to 4 decimal places:
   ```json
   {
     "correlation_f3_score": -0.1234,
     "pc1_mean_ci_lower": -0.0512,
     "pc1_mean_ci_upper": 0.0512
   }
   ```

Start your service in the background and ensure it stays running. You can use `/home/user/sample.csv` (which you will need to create yourself to test) for local testing.