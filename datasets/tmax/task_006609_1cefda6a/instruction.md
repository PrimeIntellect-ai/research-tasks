I need your help automating a data cleaning pipeline for some dirty sensor data I just received. 

I have a file at `/home/user/raw_data.csv` containing time-series data with three columns: `timestamp`, `sensor_id`, and `value`. 

Please do the following:
1. Write a Python script at `/home/user/cleaner.py` that processes this CSV file.
2. In the script, implement **hash-based deduplication**. Specifically, create a new column called `row_hash` that contains the MD5 hex digest of the comma-joined string of the three original columns (e.g., `md5("2023-10-01T10:00:00,A,10.0".encode('utf-8')).hexdigest()`). If the `value` is missing/empty, it should hash the string with the empty value (e.g., `"2023-10-01T10:01:00,A,"`). Drop any rows that have a duplicate `row_hash`, keeping the first occurrence. Afterwards, drop the `row_hash` column.
3. After deduplicating, parse the `timestamp` column as datetime and sort the dataset chronologically.
4. Perform **linear time-based interpolation** on the `value` column to fill in any missing (`NaN` or empty) values. Round the interpolated values to 1 decimal place.
5. Save the cleaned dataset to `/home/user/clean_data.csv`, preserving the original column order (`timestamp`, `sensor_id`, `value`). Ensure the `timestamp` is formatted as an ISO8601 string (e.g., `YYYY-MM-DDTHH:MM:SS`).
6. Run the script once to generate the output file.
7. Finally, schedule this script to run automatically using `cron`. Add a cron job for the current user that executes `python3 /home/user/cleaner.py` every hour at exactly the 15th minute. 
8. Save a backup of the updated crontab to `/home/user/cron_backup.txt` using `crontab -l > /home/user/cron_backup.txt`.