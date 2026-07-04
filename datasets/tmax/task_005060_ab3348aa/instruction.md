You are a data scientist tasked with cleaning a set of sensor datasets that have been corrupted by a buggy ETL job. The ETL job occasionally retried and produced duplicate records, but only during specific maintenance windows. 

First, we have an audio recording from the system operator, located at `/app/operator_notes.wav`. You need to transcribe this audio file (you can install and use `whisper` or similar tools) to determine the exact hours when the ETL retries occurred.

Second, you need to build a robust Python data filter. The datasets are stored in CSV files in a wide format (each row is a timestamp, and columns are sensor1, sensor2, ... sensor10). 
Your script must:
1. Reshape the data from wide to long format.
2. Apply a rolling window aggregation (window size of 5) to smooth the sensor readings.
3. Detect anomalies and changepoints (specifically, if the rolling average jumps by more than 50% between consecutive windows, or if there are exact duplicate time blocks within the operator's maintenance windows).

You must write a script at `/home/user/classifier.py` that can be run as follows:
`python3 /home/user/classifier.py <path_to_csv>`

The script must exit with code `0` if the file is clean (valid data, no anomalies, no duplicate retry blocks), and exit with code `1` if the file is "evil" (contains anomalies, changepoints, or duplicated retry blocks).

We have provided a small sample of clean and corrupted datasets in `/app/data/sample_clean/` and `/app/data/sample_evil/` for you to test your logic. The final automated evaluation will run your script against a hidden set of files. Your script must correctly classify all files in the hidden sets.