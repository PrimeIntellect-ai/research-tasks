You are an ML Engineer tasked with preparing training data for a user behavior model. You have three large datasets extracted from different systems, but the previous data pipeline was silently corrupting the features due to improper handling of missing values during joins (e.g., missing values were shifted or converted to 0 incorrectly, ruining the statistical distribution).

Your goal is to write a robust Bash script at `/home/user/process_data.sh` that securely joins the data, engineers the missing features, and calculates a baseline correlation.

The datasets are located in `/home/user/data/`:
1. `users.csv` - Contains all users. Columns: `user_id,age`
2. `purchases.csv` - Contains purchase data. Columns: `user_id,purchase_amount`. (Note: Not all users have made a purchase. Some users are missing from this file).
3. `activity.csv` - Contains login counts. Columns: `user_id,login_count`. (Note: Not all users are present here either).

Your script `/home/user/process_data.sh` must perform the following actions when executed:
1. Join the three datasets on `user_id` using a left join (keeping all users from `users.csv`).
2. If a user is missing from `purchases.csv`, their `purchase_amount` must be represented as the string `NaN`.
3. If a user is missing from `activity.csv`, their `login_count` must be represented as `0` (imputation by 0).
4. Save the cleanly joined output to `/home/user/features.csv` with the exact header: `user_id,age,purchase_amount,login_count`. The rows must be sorted by `user_id` numerically.
5. Extract all rows where `purchase_amount` is NOT `NaN`. Using Python (which you can invoke from your bash script), calculate the Pearson correlation coefficient between `age` and `purchase_amount` for these valid rows. 
6. Save the Pearson correlation coefficient, rounded to exactly 4 decimal places, to `/home/user/correlation.txt`.

Constraints:
- You must write the main logic in `/home/user/process_data.sh`.
- You can use standard Linux tools (awk, join, sed, sort) and invoke Python for the statistical math. 
- Ensure your script is executable.

To complete the task, execute your script so that `/home/user/features.csv` and `/home/user/correlation.txt` are created.