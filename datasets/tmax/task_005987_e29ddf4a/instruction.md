You are a Data Scientist working in a minimal Linux environment where Python and R are unavailable. You need to clean a server metrics dataset and perform exploratory statistical analysis using only standard shell tools (Bash, awk, grep, coreutils).

The dataset is located at `/home/user/metrics.csv`. It has a header row and the following 7 columns:
`ID,CPU,Memory,Response_Time,Const1,Const2,Status`

Your task is to create a shell script at `/home/user/analyze.sh` that processes this CSV file to compute several statistical metrics. The script must perform the following:

1. **Numerical Configuration:** Ensure consistent decimal formatting by exporting `LC_NUMERIC=C`.
2. **Data Cleaning:** Filter the dataset to include only valid data rows. A valid row must:
   - Not be the header.
   - Have exactly 7 columns.
   - Have `OK` in the `Status` column (Column 7).
   - Not contain the string `NaN` or any empty fields in any column.
3. **Dimensionality Reduction (Zero-Variance Columns):** Identify which columns have zero variance (i.e., the value is constant across all cleaned rows). Write the 1-indexed column numbers as a comma-separated list to `/home/user/zero_variance_cols.txt` (e.g., `5,6`).
4. **Correlation Analysis:** Calculate the Pearson correlation coefficient between `CPU` (Column 2) and `Memory` (Column 3) for the cleaned data. Write the result, rounded to exactly 3 decimal places, to `/home/user/correlation.txt`.
5. **Hypothesis Testing / Confidence Intervals:** Calculate the sample mean and the 95% Confidence Interval for the `Response_Time` (Column 4) of the cleaned data.
   - Use the sample standard deviation (divided by n-1).
   - Use 1.96 as the z-score multiplier for the 95% CI.
   - Write the output as `Mean,Lower,Upper`, each rounded to exactly 3 decimal places, to `/home/user/ci.txt`.

Constraints:
- You must write your logic strictly in Bash using built-in commands and standard utilities like `awk`, `sed`, `grep`, `bc`, etc.
- Do NOT use Python, R, Perl, or any other higher-level scripting languages.
- You can execute your script to generate the output files and verify them.