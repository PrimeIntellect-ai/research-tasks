You are acting as a localization engineer. We need to prioritize updating translations for UI elements based on recent user activity. You have been given raw user interaction logs, a localization mapping file, and a request template. Your task is to process the time series log data, compute rolling usage statistics, and generate a translation request document for the translation team.

Here is the setup:

1. **Input Data:**
   - `/home/user/logs/ui_events.csv`: A messy CSV file containing `timestamp`, `user_id`, and `element_id`. Some rows are duplicated, and some are missing `element_id` or `timestamp`.
   - `/home/user/loc/mapping.json`: A JSON file mapping `element_id` to a `loc_key` (localization string identifier).
   - `/home/user/templates/request_template.txt`: A text file containing a template for the translation request.

2. **Data Cleaning & Normalization:**
   - Read the CSV file.
   - Drop any rows missing a `timestamp` or `element_id`.
   - Deduplicate exact row matches (if `timestamp`, `user_id`, and `element_id` are identical, keep only one).
   - Parse the `timestamp` as a date (ignore time/timezone, bucket by day).

3. **Time Series Aggregation & Rolling Stats:**
   - Aggregate the total count of events per day for each `element_id`.
   - Compute a 3-day rolling average of the event count for each `element_id` (this means the average of the current day and the two preceding days). If an `element_id` has missing days, treat the count for those days as 0 before calculating the rolling average. Use `min_periods=1`.

4. **Localization Mapping & Output Generation:**
   - For the date `2023-10-15`, find the top 3 `element_id`s with the highest 3-day rolling average. (In case of a tie, sort by `element_id` alphabetically).
   - Map these `element_id`s to their corresponding `loc_key` using `mapping.json`.
   - Generate a markdown file at `/home/user/translation_requests.md` using the exact text from `/home/user/templates/request_template.txt`. Replace the placeholder `{KEYS}` with the top 3 `loc_key`s, separated by commas, in descending order of their rolling average (and alphabetical for ties).

Write a Python script to perform this ETL pipeline and generate the final file.