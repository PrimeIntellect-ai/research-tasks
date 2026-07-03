You are an analyst tasked with processing a mix of sensor data and system logs. We have a SQLite database containing numerical sensor readings with missing timeframes, and a JSON-Lines file containing textual logs. 

Unfortunately, the logging system had a bug and generated malformed unicode escape sequences in the JSON-Lines file (e.g., `\uZZZZ`), causing standard JSON parsers to crash.

Your objective is to clean the data, impute missing values, tokenize the logs, and join the datasets into a single CSV file.

Here are your instructions:

1. **Process the Logs (`/home/user/logs.jsonl`)**
   - The file contains JSON lines, each with a `ts` (timestamp string) and a `msg` (text string).
   - Some `msg` fields contain malformed unicode escapes (like `\u00XX` where XX is invalid hex). You must parse the file safely, stripping or ignoring the malformed escapes so you can extract the text.
   - For each valid message, **tokenize** the text:
     - Convert the string to lowercase.
     - Remove all non-alphanumeric characters (keep spaces).
     - Split by space to get a list of tokens.
     - Discard empty tokens.
   - Truncate the `ts` timestamp to the start of the hour (e.g., `2023-10-01 10:15:00` becomes `2023-10-01 10:00:00`).
   - Aggregate the total number of valid tokens per hour.

2. **Process the Sensor Data (`/home/user/sensors.db`)**
   - The SQLite database contains a table `readings` with columns `timestamp` (TEXT, e.g., `2023-10-01 10:00:00`) and `temp` (REAL).
   - The data is missing entries for several hours.
   - Resample the data to an hourly frequency and use **linear interpolation** to fill in the missing `temp` values for hours that fall between existing data points.

3. **Merge and Export**
   - Perform an **inner join** on the hourly timestamps between the interpolated sensor data and the aggregated hourly token counts.
   - Export the merged data to `/home/user/merged_output.csv`.
   - The CSV must have exactly these columns, in this order: `hour`, `temp`, `token_count`.
   - Include a header row.
   - Format the `temp` values to exactly one decimal place.
   - Sort the CSV chronologically by `hour`.

You may use Python and standard data science libraries (e.g., `pandas`, `sqlite3`, `re`, `json`) to complete this task. Write your scripts and execute them in the terminal.