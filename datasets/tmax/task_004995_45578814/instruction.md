I need help cleaning and sampling a dataset for my analysis. I have two data files in different formats that need to be joined, stratified, sampled, and then exported into a local SQLite database.

Here are the details of the files:
1. `/home/user/telemetry.csv`: A CSV file containing event logs. Columns: `user_id`, `event_type`, `timestamp`, `region`.
2. `/home/user/users.json`: A JSON file containing an array of user objects. Each object has keys `user_id` and `subscription_tier`.

Please write and execute a Python script to perform the following steps:
1. Read both files.
2. Perform an inner join on `user_id` (discard any telemetry events that do not have a corresponding user in the JSON file).
3. Stratify the joined dataset by `subscription_tier`.
4. Within each `subscription_tier` stratum, sort the records first by `timestamp` in ascending order, and then by `user_id` in ascending order.
5. Take a deterministic 50% sample from each stratum. Specifically, using 0-based indexing for the sorted records in each stratum, select the records at even indices (index 0, 2, 4, 6...).
6. Save the sampled records into a new SQLite database located at `/home/user/cleaned_sample.db`. 
7. The data should be inserted into a table named `telemetry_sample` with the following columns (in this exact order): `user_id` (TEXT), `event_type` (TEXT), `timestamp` (TEXT), `region` (TEXT), `subscription_tier` (TEXT).

Ensure the final SQLite database exists at the specified path and has the correctly populated table.