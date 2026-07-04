You are a data scientist cleaning a messy sensor log file. I have a log file located at `/home/user/raw_data.txt`. 

The file is a pipe-separated (`|`) text file with four columns:
1. **Timestamp**: A string representing the time the reading was taken (in UTC). Formats vary between standard SQL format (e.g., `2023-11-01 08:00:00 UTC`) and ISO 8601 (e.g., `2023-11-01T08:01:00Z`).
2. **Sensor ID**: A string identifier for the sensor, with inconsistent casing.
3. **Value**: A numeric reading.
4. **Remarks**: Free-form text notes from the system, containing mixed casing and noisy punctuation.

I need you to write and execute a Bash script at `/home/user/process.sh` that reads this file and transforms it into a clean, comma-separated values (CSV) file at `/home/user/cleaned_data.csv` without a header row.

Your transformation must perform the following:
- **Timestamp alignment**: Convert the timestamp into a UNIX Epoch timestamp.
- **Normalization**: 
  - Convert the **Sensor ID** to strictly UPPERCASE and trim any surrounding whitespace.
  - Clean the **Remarks** column by: removing all non-alphanumeric characters (except spaces), converting the text to UPPERCASE, and trimming any leading/trailing whitespace. Multiple spaces between words should be left as-is.
- **Rolling Statistics**: Add a 5th column to the CSV containing a rolling moving average of the **Value** column for the *current row and up to two previous rows* (i.e., a maximum window size of 3). If fewer than 3 rows exist (e.g., for the first two rows), compute the average of the available rows. This rolling average must be formatted to exactly two decimal places.

**Target Output Format (`/home/user/cleaned_data.csv`):**
`EpochTimestamp,SensorID,Value,CleanedRemarks,RollingAvg`

Do not add a header row to the output CSV. Make sure your script handles the file directly and processes it completely.