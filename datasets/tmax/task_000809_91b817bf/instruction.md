You are a data scientist cleaning a global sensor dataset. The data pipeline team has staged a raw archive from our international sensor network in a remote-equivalent staging directory at `/tmp/staging/sensor_archive.tar.gz`.

Your goal is to write a robust Bash script (you may use standard Linux utilities like `awk`, `sed`, `iconv`, etc., or inline Python/Perl within the bash script) to automate the cleaning and transformation of this data. 

Here are your instructions:

1. **Local-Remote Transfer**: Extract the archive from `/tmp/staging/sensor_archive.tar.gz` into your working directory `/home/user/workspace/`. It contains a single file: `raw_sensors.csv`.
2. **Character Encoding**: The file `raw_sensors.csv` is exported from a legacy Windows system in UTF-16LE encoding. Convert it to standard UTF-8.
3. **Wide-to-Long Reshaping**: The CSV is currently in a wide format. 
   - Column 1: `Date` (format YYYY-MM-DD)
   - Columns 2+: `<City>_<MetricLocal>`
   You need to reshape this into a long-format dataset.
4. **Multi-language Text Processing**: The metrics in the column headers are in the local languages of the sensors. You must translate them into standard English. 
   - `温度` (Japanese) -> `Temperature`
   - `Température` (French) -> `Temperature`
   - `Влажность` (Russian) -> `Humidity`
   - Existing English terms like `Temperature` and `Humidity` should remain as is.
5. **Feature Extraction**: Create two new columns, `Year` and `Month`, extracted from the `Date` column.

**Final Output Specification:**
Your script must produce a clean CSV file located at `/home/user/workspace/clean_timeseries.csv`.
The file must have exactly the following header (comma-separated):
`Year,Month,Date,City,Metric,Value`

The data rows should follow this structure (example):
`2023,01,2023-01-15,Tokyo,Temperature,8.1`

Sort the final CSV data (excluding the header) alphabetically by `Date`, then `City`, then `Metric`. Ensure the final file is valid UTF-8 and uses Unix-style (LF) line endings.

Create and run your script to generate the final `clean_timeseries.csv` file.