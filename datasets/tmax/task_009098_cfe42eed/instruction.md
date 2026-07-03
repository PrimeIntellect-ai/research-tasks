You are a data scientist building a reproducible data cleaning and feature engineering pipeline.

You have a raw dataset located at `/home/user/raw_data.csv` with the following columns: `id,sensor_x,sensor_y,target_val`.

Your task is to write a Bash shell script named `/home/user/run_pipeline.sh` that processes this dataset. The script can use standard Unix utilities (like `awk`, `sed`, `grep`, `bc`) or inline Python/Perl scripts if necessary, but the pipeline execution must be contained within this single Bash script.

The script must perform the following steps:
1. **Data Cleaning**: Read `/home/user/raw_data.csv`. Skip the header. Filter out any rows where `sensor_y` is exactly `0` or `0.0` to avoid division-by-zero errors in the next step.
2. **Feature Engineering**: For the remaining rows, calculate a new feature `ratio_z` = `sensor_x` / `sensor_y`. 
3. **Save Cleaned Data**: Output the cleaned and augmented dataset to `/home/user/cleaned_data.csv`. This file must not have a header row. It must be a comma-separated file with the columns in this exact order: `id,sensor_x,sensor_y,ratio_z,target_val`. Ensure `ratio_z` is computed accurately.
4. **Correlation Analysis**: Compute the Pearson correlation coefficient between the newly engineered feature `ratio_z` and `target_val` using the cleaned data.
5. **Numerical Accuracy & Output**: Save the computed Pearson correlation coefficient to a file named `/home/user/correlation.txt`. The file must contain only the correlation coefficient, rounded to exactly 4 decimal places (e.g., `0.8523` or `-0.1200`).

Requirements:
- Make sure your script `/home/user/run_pipeline.sh` is executable.
- Run your script so that `/home/user/cleaned_data.csv` and `/home/user/correlation.txt` are generated.
- Your pipeline must be perfectly reproducible (running it multiple times should yield the exact same output).