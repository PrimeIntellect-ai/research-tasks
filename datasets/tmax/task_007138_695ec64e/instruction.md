You are an AI assistant helping a climate researcher organize a dataset collected from an older environmental sensor. 

The researcher has uploaded a raw log file located at `/home/user/raw_sensor.log`. Unfortunately, it has a few issues that need to be resolved before analysis:
1. The file was exported from an old Windows-based system and is encoded in UTF-16LE.
2. The file contains carriage returns (`\r`) and inconsistent leading/trailing spaces on the lines.
3. The logs are formatted as multi-line records rather than a standard tabular format.

Your task is to process this data through the following steps:

1. **Encoding Conversion**: Convert the file `/home/user/raw_sensor.log` from UTF-16LE to UTF-8. Save the result as `/home/user/sensor_utf8.log`.
2. **Text Transformation**: Using command-line tools like `sed` or `awk`, process `/home/user/sensor_utf8.log` to:
   - Remove all carriage return (`\r`) characters.
   - Remove any leading and trailing spaces from every line.
   - Save the cleaned output to `/home/user/sensor_clean.log`.
3. **Multi-line Parsing**: Write a C++ program (save it as `/home/user/parse_logs.cpp`) to parse the multi-line records in `/home/user/sensor_clean.log`. 
   - Each record starts with the line `[BEGIN]` and ends with the line `[END]`.
   - Inside the record, there are key-value pairs separated by a colon and a space (e.g., `Timestamp: 2023-05-12 08:00:00`).
   - The fields are `Timestamp`, `Station`, `Temp`, and `FaultCode`.
   - Your C++ program must extract these fields, skip any record where `FaultCode` is not exactly `0`, and write the valid records to a CSV file at `/home/user/clean_data.csv`.
   - The CSV must have the exact header: `Timestamp,Station,Temp`
   - The CSV rows must correspond to the valid records in the order they appear.

Compile your C++ program and run it to produce `/home/user/clean_data.csv`. Keep the intermediary files (`sensor_utf8.log` and `sensor_clean.log`) on the disk.