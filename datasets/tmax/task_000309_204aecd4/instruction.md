You are a Data Scientist cleaning a raw dataset using command-line tools. You have two data sources stored as CSV files:
- `/home/user/source1.csv` (Columns: `id`, `feature_x`)
- `/home/user/source2.csv` (Columns: `id`, `feature_y`)

These files contain messy data: some values are missing entirely (empty strings), and some are sensor errors (extreme outliers). 

Your task is to write a Bash script named `/home/user/clean_and_correlate.sh` that performs the following steps when executed:
1. **Multi-source Data Joining**: Join the two datasets on the `id` column. Assume the files might not be sorted.
2. **Missing Value & Outlier Handling**: Filter the joined data to remove any rows where `feature_x` or `feature_y` is missing (empty). Also, remove any rows where either feature is strictly greater than `50.0` or strictly less than `-50.0`.
3. **Output Cleaned Data**: Save the cleaned pairs of `feature_x` and `feature_y` (comma-separated, without the `id` column or headers) to `/home/user/cleaned_features.csv`.
4. **Correlation Analysis**: Calculate the Pearson correlation coefficient between the cleaned `feature_x` and `feature_y`. Write this single numeric value, rounded to 3 decimal places, to `/home/user/correlation.txt`.

You may use standard Linux command-line tools (like `join`, `awk`, `sort`, `sed`) and you are permitted to use a `python3` one-liner or inline script within your Bash script if you find calculating the Pearson correlation in pure Bash or `awk` too cumbersome.

Make sure your script `/home/user/clean_and_correlate.sh` is executable and successfully creates the required files when run.