You are acting as a data scientist cleaning up a messy dataset. An ETL job failed halfway and was retried, resulting in two split CSV files with overlapping, duplicate records. 

Your task is to write a Python script at `/home/user/process.py` that processes these files, and then schedule it using cron.

**Data Inputs:**
You have two CSV files:
1. `/home/user/data/users_run1.csv`
2. `/home/user/data/users_run2.csv`

**Processing Requirements:**
Write a Python script (`/home/user/process.py`) using the standard library or `pandas` to perform the following operations:
1. **Union and Deduplicate:** Combine both datasets. Remove duplicate rows based on the `user_id` column. If there are duplicates, keep the first occurrence.
2. **Normalize Dates:** The `signup_date` column has mixed formats (e.g., `MM/DD/YYYY`, `YYYY-MM-DD`, `MM-DD-YYYY`). Normalize all of them to the ISO format: `YYYY-MM-DD`.
3. **Mask Emails:** Anonymize the `email` column. Replace all characters in the local part (before the `@`) with asterisks (`*`), EXCEPT for the last two characters. For example, `alice.smith@example.com` becomes `*********th@example.com`. If the local part is 2 characters or fewer, leave it unmasked.
4. **Export:** Save the cleaned, combined dataset to `/home/user/clean_users.csv`. The output CSV must include the headers and be sorted by `user_id` in ascending numerical order.

**Scheduling:**
Once the script is written, you must:
1. Make the script executable.
2. Run the script once to generate `/home/user/clean_users.csv`.
3. Set up a cron job for the current user to run `/home/user/process.py` every day at 2:00 AM.
4. Save the output of `crontab -l` to `/home/user/cron_backup.txt` so your scheduling can be verified.