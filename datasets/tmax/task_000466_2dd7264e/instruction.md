You are a data analyst managing event logs for a web application. The raw data is taking up too much active storage, and we need to aggregate user activity while cleaning out bad records, then archive the raw data.

Your workspace contains a directory `/home/user/events/` which holds several CSV files containing raw event logs. 
The CSV files have no headers. The columns are: `user_id,event_type,duration,timestamp`.

Write and execute a Bash script (or run shell commands directly) to perform the following pipeline:

1. **Data Cleaning & Filtering**: Read through all `.csv` files in the `/home/user/events/` directory. Drop any rows where the `duration` (the 3rd column) is:
   - Missing (empty string)
   - Less than 0
   - Greater than 5000 (which we consider an outlier)

2. **Aggregation**: For the valid rows, compute the total sum of `duration` for each `user_id`.

3. **Output**: Save the aggregated results to a new file at `/home/user/user_durations.csv`. 
   - The format must be exactly `user_id,total_duration`.
   - The file must be sorted by `total_duration` in strictly descending order (highest duration first).
   - Do not include headers in the output.

4. **Storage Management**: 
   - Compress the entire `/home/user/events/` directory into a gzip-compressed tarball located at `/home/user/events_archive.tar.gz`. The tarball should contain the `events/` directory at its root.
   - Delete the original `/home/user/events/` directory after successfully archiving it.

Ensure your entire solution can be accomplished via the Bash command line.