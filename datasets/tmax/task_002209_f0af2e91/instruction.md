You are acting as an AI assistant for a data scientist who needs to automate the cleaning of some legacy sensor data. 

We receive a daily TSV (tab-separated) file at `/home/user/raw_data.tsv`. The file has three columns:
1. `Hour` (integer, representing the hour offset from the start of the experiment)
2. `Value` (float, the sensor measurement)
3. `Metadata` (string, the sensor name/metadata)

There are three problems with this data:
1. **Missing Data (Gaps):** Some hours are skipped. We need to regularize the time series to have exactly one entry per hour from the minimum hour to the maximum hour present in the file. Use **forward-fill** for the missing `Value` and `Metadata` (i.e., use the values from the most recent available hour). 
2. **Character Encoding:** The `Metadata` string sometimes contains non-ASCII characters (like legacy ISO-8859-1 bytes) that break our downstream JSON parsers.
3. **Lack of Summaries:** We need basic statistics over the *gap-filled* data.

Your task is to:
1. Write a C++ program at `/home/user/process_data.cpp` that reads `/home/user/raw_data.tsv`.
2. Clean the `Metadata` strings by replacing any non-ASCII character (byte values > 127 or < 32, except standard whitespace like tab/newline if applicable, though the metadata itself won't contain tabs) with a question mark (`?`).
3. Fill in the missing hours using forward-fill for the missing values.
4. Calculate the Minimum, Maximum, and Mean of the `Value` column over the fully gap-filled dataset.
5. The C++ program must output a report exactly matching this template to `/home/user/report.txt`:
```
Data Report
-----------
Cleaned Metadata: [The cleaned metadata string of the very last record]
Total Records: [Count of records after gap-filling]
Min: [Minimum value, formatted to 2 decimal places]
Max: [Maximum value, formatted to 2 decimal places]
Mean: [Mean value, formatted to 2 decimal places]
```
6. Compile your C++ program to `/home/user/process_data`.
7. Configure the user's crontab to run this executable `/home/user/process_data` every day at exactly 03:15 AM.

You may assume the input file is small (under 1000 lines) and the hours are strictly increasing. Compile the code using `g++ -O2 /home/user/process_data.cpp -o /home/user/process_data`.