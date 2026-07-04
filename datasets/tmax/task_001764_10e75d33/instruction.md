You are an automation specialist managing data pipelines for an IoT sensor network. 

You need to write a high-performance C program that processes a daily raw data dump. The input data is in a "wide" CSV format with embedded event logs, but contains duplicate transmissions. You must reshape it into a clean "long" format, normalize the logs, and deduplicate entries.

**Task Requirements:**
1. Create a C program at `/home/user/process_data.c`.
2. The program must read an input CSV file located at `/home/user/raw_sensors.csv`.
3. The input file has the following header and format:
   `sensor_id,timestamp,metric_A,metric_B,event_log`
   - `sensor_id`: string (max 16 chars)
   - `timestamp`: long integer
   - `metric_A`: float
   - `metric_B`: float
   - `event_log`: string containing semicolon-separated tags (e.g., `SystemBoot;OK;v1.2`)
4. **Deduplication:** The network sometimes sends duplicate transmissions. If you encounter a row with a `sensor_id` and `timestamp` combination that has *already been seen* in the file, completely ignore the duplicate row.
5. **Tokenization & Normalization:** For the `event_log` field, extract *only* the first token (everything before the first `;`). If there is no `;`, take the whole string. Convert this extracted token to strictly lowercase.
6. **Wide-to-Long Reshaping:** For each valid, deduplicated row, output *two* rows into the output CSV: one for `metric_A` and one for `metric_B`.
7. The output file must be written to `/home/user/clean_telemetry.csv` with the following format (no header):
   `sensor_id,timestamp,metric_name,metric_value,normalized_event`
   - `metric_name` must be exactly the string `metric_A` or `metric_B`.
   - `metric_value` must be formatted to exactly 2 decimal places.

**Example Input:**
```csv
sensor_id,timestamp,metric_A,metric_B,event_log
S01,1600000000,22.5,45.1,BOOT_SEQ;SUCCESS
S02,1600000005,19.2,40.0,Warn;LowBattery
S01,1600000000,99.9,99.9,FAKE;DATA
```

**Example Output:**
```csv
S01,1600000000,metric_A,22.50,boot_seq
S01,1600000000,metric_B,45.10,boot_seq
S02,1600000005,metric_A,19.20,warn
S02,1600000005,metric_B,40.00,warn
```
*(Note that the duplicate S01 at 1600000000 was ignored).*

Compile your program using `gcc -O3 -o /home/user/processor /home/user/process_data.c` and execute it to generate the final `clean_telemetry.csv` file. Do not use external libraries other than the standard C library.