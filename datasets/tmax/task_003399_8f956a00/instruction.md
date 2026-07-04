You are a data engineer troubleshooting an ETL pipeline. 

There is an existing Python script located at `/home/user/etl.py`. This script reads two datasets (`/home/user/profiles.csv` and `/home/user/logs.csv`), merges them, computes a user similarity matrix based on Pearson correlation of their features, writes the top 3 most similar users to a target user into a text file, and saves the final merged dataset to a Parquet file for large-scale storage.

However, the pipeline has a silent bug: because some users in the logs don't have profiles, the pandas merge operation introduces `NaN` values. This silently promotes the `user_id` and feature columns from integers to floats. Consequently, the downstream Parquet file is saved with `float64` schemas for columns that should be strictly integers, and the correlation matrix contains `NaN` outputs that skew similarity searches.

Your task is to fix `/home/user/etl.py` to satisfy these requirements:
1. Perform the merge as currently implemented, but fill any missing feature values (from missing profiles) with `0`.
2. Ensure that ALL columns in the final merged DataFrame (`user_id`, `feat1`, `feat2`, `feat3`, `activity_score`) are explicitly cast to standard pandas `int64` types.
3. Compute the Pearson correlation matrix on the transposed feature columns (excluding `activity_score`) to find the top 3 users most similar to `user_id=100`.
4. Save the corrected DataFrame to `/home/user/output.parquet`.
5. Write the top 3 similar `user_id`s (as integers, comma-separated, descending order of similarity, excluding the target user 100 itself) to `/home/user/similar_users.txt`.

Run the fixed script so that the correct Parquet file and text file are generated.