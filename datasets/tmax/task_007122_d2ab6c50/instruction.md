You are a data scientist cleaning up a user database. You have two datasets:
1. `/home/user/users.csv` containing `user_id`, `name`, and `age`.
2. `/home/user/scores.csv` containing `user_id`, `score1`, and `score2`.

Write a Python script at `/home/user/join_data.py` that performs the following pipeline:
1. Reads both CSV files using `pandas`.
2. Performs a left join, keeping all records from `users.csv`.
3. Fills any missing values in the `score1` and `score2` columns with `0`.
4. Creates a new feature called `total_score` which is the sum of `score1` and `score2`.
5. Enforces a strict integer schema: the columns `user_id`, `age`, `score1`, `score2`, and `total_score` MUST be integers. (Beware: Pandas silently converts integer columns to floats when NaNs are introduced during a join. You must fix this so the final CSV has no `.0` decimals).
6. Outputs the final dataframe to `/home/user/merged.csv` without the index (`index=False`).

Run your script to generate `/home/user/merged.csv`.