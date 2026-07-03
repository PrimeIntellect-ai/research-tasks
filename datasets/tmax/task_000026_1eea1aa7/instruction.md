You are a log analyst investigating server event patterns. We have a raw server log export at `/home/user/raw_server_logs.csv` that previous analysts struggled with because some multi-language system messages contain embedded newlines and commas, breaking naive text-processing pipelines.

Your task is to write and execute a Python script that robustly processes this data, extracting temporal and mathematical patterns, and outputs the result to `/home/user/rolling_metrics.csv`.

Here are the specific requirements:

1. **Parse and Reshape**: 
   The input CSV has the following columns: `timestamp, msg_en, msg_es, msg_zh, msg_ru`. 
   Read the CSV correctly, handling embedded newlines and Unicode characters. Reshape the data from this wide format into a long format with columns: `timestamp, language, message`. The `language` column should contain the suffix (e.g., 'en', 'es', 'zh', 'ru'). Drop rows in the long format where the `message` is empty or NaN.

2. **Resample and Gap-Fill**:
   Convert the `timestamp` column to a standard Python/Pandas Datetime type.
   Group the data by `language` and resample the event counts (number of messages) into strictly 15-minute intervals (using the start of the interval, e.g., 10:00:00, 10:15:00). 
   If a language has no events in a particular 15-minute interval within the global minimum and maximum timestamps of the entire dataset, you must fill that gap with a count of `0`.

3. **Windowed Aggregation**:
   For each language, calculate a rolling average of the 15-minute event counts using a window size of 3 intervals. 
   Use `min_periods=1` so that the first and second intervals yield valid averages rather than NaNs. Round the rolling average to 2 decimal places.

4. **Output Specifications**:
   Save the final dataset to `/home/user/rolling_metrics.csv` with exactly these columns:
   `timestamp, language, message_count, rolling_avg`
   Sort the CSV first by `language` (alphabetically: en, es, ru, zh), and then by `timestamp` (chronologically).
   Format the `timestamp` column as `YYYY-MM-DD HH:MM:SS`. 

Do not rely on naive `\n` splitting for the initial file, as the embedded newlines in the multi-language text fields will corrupt the columns. Use robust CSV parsing (like pandas `read_csv` or the `csv` module).