You are an AI assistant helping an environmental researcher organize their workspace and analyze a newly collected dataset. 

The researcher has two raw data files located at:
- `/home/user/raw_data/sensor_A.csv` (contains columns: `timestamp`, `temp`, `humidity`)
- `/home/user/raw_data/sensor_B.csv` (contains columns: `timestamp`, `pressure`, `radiation`)

Please perform the following tasks:
1. **Analysis Environment Setup:** Create a new directory at `/home/user/analysis_env` for the analysis outputs.
2. **Data Integration:** Merge the two datasets based on the `timestamp` column. Sort the merged dataset chronologically (ascending `timestamp`).
3. **Outlier Handling:** Due to known sensor glitches, any `temp` values strictly greater than 100.0 or strictly less than -50.0 should be treated as invalid. Replace these outlier values with `NaN` (missing values).
4. **Missing Value Handling:** After removing outliers, use forward filling (ffill) to fill any missing values (`NaN`) across all metric columns (`temp`, `humidity`, `pressure`, `radiation`). Assume the first row never contains missing or outlier values.
5. **Correlation Analysis:** Calculate the Pearson correlation matrix for the four metric columns (`temp`, `humidity`, `pressure`, `radiation`).
6. **Reporting:** Identify the pair of *distinct* variables that have the highest *absolute* correlation. Write this pair and their original (signed) correlation value to `/home/user/analysis_env/highest_correlation.txt`. The format must be exactly: `var1,var2,0.XXX` (round the correlation value to exactly 3 decimal places). The variable names (`var1` and `var2`) must be in alphabetical order (e.g., `humidity,temp,0.852`).
7. **Storage Management:** To save space, archive the original `/home/user/raw_data/` directory into a tarball at `/home/user/storage_archive/raw_data.tar.gz`. (Create the `/home/user/storage_archive/` directory first). Finally, delete the `/home/user/raw_data/` directory entirely.

You may use any programming language (Python, R, etc.) and shell commands to accomplish this.