I need you to create a robust ETL pipeline script in Bash that processes raw metrics data, performs feature engineering, and calculates a statistical correlation based on a bootstrap sample. 

We have a raw dataset located at `/home/user/metrics.csv` with the following columns:
`user_id,feature_x,feature_y,target`

Some data sources have injected empty strings into the `user_id` column. In previous pipelines, this silently caused `pandas` to convert the entire `user_id` column from integers to floats (due to NaN introduction), breaking downstream joins. 

You need to write a Bash script named `/home/user/run_pipeline.sh` that performs the following steps. You may use standard Linux tools (like `awk`, `sed`, `shuf`) and/or inline Python (`python3` with `pandas`/`numpy`) within your Bash script to achieve this:

1. **Clean the Data**: Read `/home/user/metrics.csv`. Remove any rows where `user_id` is missing (empty) or where `feature_y` is equal to `0` or `0.0` (to prevent division by zero). Also ensure you handle the header correctly.
2. **Feature Engineering**: For the cleaned rows, create a new feature called `ratio` which is the result of `feature_x / feature_y`. 
3. **Bootstrap Sampling**: From the cleaned dataset (with the new `ratio` feature), draw a random sample with replacement of exactly `2000` rows. 
   *CRITICAL:* If you use Python for this sampling step, you must use `pandas.DataFrame.sample(n=2000, replace=True, random_state=42)` to ensure reproducibility.
4. **Correlation Analysis**: Calculate the Pearson correlation coefficient between the engineered `ratio` column and the `target` column based on this bootstrap sample.
5. **Output**: Print ONLY the final correlation coefficient rounded to 4 decimal places (e.g., `0.1234` or `-0.5678`) and save it to `/home/user/output.txt`.

Make sure `/home/user/run_pipeline.sh` is executable. The script should run without requiring any arguments and cleanly exit with code 0.