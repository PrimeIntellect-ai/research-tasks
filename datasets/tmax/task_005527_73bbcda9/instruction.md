You are a data scientist tasked with cleaning a messy dataset of international sensor readings. The data pipeline you are taking over has a major bug: it silently drops rows containing embedded newlines in CSV text fields or fails to parse them. You need to write a robust C program to process this file, and then load the clean data into an SQLite database.

Your input file is located at `/home/user/raw_sensors.csv`. 
It has a header: `timestamp,sensor_value,location_desc`
- `timestamp`: integer
- `sensor_value`: float
- `location_desc`: UTF-8 string, enclosed in double quotes. **Warning:** This field can contain embedded newline characters (`\n`), which are valid inside quotes according to RFC 4180.

Write a C program (save it as `/home/user/cleaner.c` and compile to `/home/user/cleaner`) that reads `raw_sensors.csv` and performs the following operations in order:

1. **Robust CSV Parsing & Text Normalization:** Parse the CSV correctly, handling quoted embedded newlines. Replace any newline characters (`\n` or `\r`) that occur *inside* the `location_desc` field with a single space (` `). Strip the enclosing quotes for the output.
2. **Constraint Validation:** Drop any records where `sensor_value` is strictly less than `0.0` or strictly greater than `1000.0`. Do not include these dropped records in any subsequent steps.
3. **Resampling & Gap Filling:** Timestamps should be strictly sequential, incrementing by exactly 1. Start from the first valid timestamp. If there is a gap between two valid records (e.g., jumps from 100 to 103), generate the missing rows (101, 102). For these generated rows, carry forward the `sensor_value` and normalized `location_desc` from the *most recent valid row*.
4. **Windowed Aggregation:** Compute a 3-period simple moving average (SMA) of the `sensor_value` on the gap-filled data. The SMA at time $T$ is the average of the `sensor_value` at $T$, $T-1$, and $T-2$. If fewer than 3 periods are available (i.e., the first two rows), compute the average of the available periods.
5. **Output:** Write the processed data to `/home/user/clean_sensors.csv`. Do not include a header row. The output format must be strictly: `timestamp,sensor_value,location_desc,ma_3`.
Format `sensor_value` and `ma_3` to exactly 2 decimal places. 

After generating `/home/user/clean_sensors.csv`, use standard command-line tools to create an SQLite database at `/home/user/sensors.db`. Create a table named `cleaned_readings` with the following schema:
`timestamp INTEGER PRIMARY KEY, sensor_value REAL, location_desc TEXT, ma_3 REAL`
Import the contents of `/home/user/clean_sensors.csv` into this table.

All necessary tools (gcc, sqlite3) are available in your environment.