You are acting as a data analyst. I need you to build a Python-based data processing pipeline that processes two CSV files containing user data and activity logs.

The input files are located in `/home/user/data/`:
1. `/home/user/data/users.csv` - Contains user profiles. Columns: `user_id`, `signup_date`, `country`, `tier`
2. `/home/user/data/activity.csv` - Contains user activity logs. Columns: `timestamp`, `user_id`, `action`, `duration`

Your task is to write a Python script (e.g., `/home/user/pipeline.py`) that performs the following steps:

1. **Validation Checkpoint**: Read `activity.csv` and filter out any invalid rows. A row is invalid if:
   - `duration` is less than 0.
   - `action` is empty or missing.
   Count the number of invalid rows dropped in this step.

2. **Merge/Join**: Perform an inner join between the valid activity data and `users.csv` on `user_id`.

3. **Time-Based Bucketing**: Extract the date (YYYY-MM-DD) from the ISO8601 `timestamp` string in the activity data. 

4. **Aggregation**: Group the joined data by `date`, `country`, and `tier`. For each group, calculate:
   - `total_duration`: the sum of the `duration` column.
   - `action_count`: the number of actions in that group.

5. **Output Writing**:
   - Save the aggregated data to `/home/user/output/daily_aggregation.json` as a JSON array of objects. The objects should have keys `date`, `country`, `tier`, `total_duration`, and `action_count`. Sort the array ascending by `date`, then `country`, then `tier`.
   - Save a pipeline summary to `/home/user/output/pipeline_summary.json` containing exactly one key `"invalid_activity_rows"` mapped to the integer count of rows dropped during the Validation Checkpoint (step 1).

Make sure the `/home/user/output/` directory exists before writing files. Run your script so the outputs are generated.