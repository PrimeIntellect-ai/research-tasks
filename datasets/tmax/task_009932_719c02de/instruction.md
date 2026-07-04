You are an ETL Data Engineer. You have been given a poorly formatted CSV file containing sensor data, and you need to process it using C, then load it into an SQLite database. 

The file `/home/user/sensor_data.csv` contains telemetry logs with three columns: `timestamp` (integer seconds), `temperature` (float), and `status` (string). 
However, the system that generated this CSV allowed embedded newlines inside the quoted `status` fields, which breaks standard line-by-line parsers. Furthermore, the telemetry data drops packets, meaning there are gaps in the integer timestamps.

Your task is to write a C program at `/home/user/process_telemetry.c` that does the following:
1. Compiles to an executable named `/home/user/process_telemetry`.
2. Reads the `/home/user/sensor_data.csv` file. It must correctly parse CSV rows, even when the `status` field is enclosed in double quotes (`"`) and contains embedded newline (`\n`) characters.
3. Cleans the `status` field by replacing any embedded newline characters with a single space character. It should also strip the enclosing double quotes from the output.
4. Performs gap-filling (resampling) on the time series:
   - For any missing integer timestamp between two recorded timestamps, insert a new row.
   - The `temperature` for these inserted rows must be linearly interpolated between the known temperatures before and after the gap.
   - The `status` for all interpolated rows must be exactly the string `FILLED`.
5. Writes the cleaned and gap-filled data to a Tab-Separated Values (TSV) file at `/home/user/cleaned_telemetry.tsv`.
   - The TSV must not have a header.
   - The columns must be: `timestamp` (integer), `temperature` (formatted to exactly 2 decimal places, e.g., `%.2f`), and `status`.
   - Fields must be separated by a single tab character (`\t`).

After generating the TSV, you must use the `sqlite3` command-line tool to:
1. Create a database at `/home/user/telemetry.db`.
2. Create a table named `sensor_log` with the schema: `CREATE TABLE sensor_log (timestamp INTEGER PRIMARY KEY, temperature REAL, status TEXT);`
3. Bulk import the `/home/user/cleaned_telemetry.tsv` file into the `sensor_log` table.

Constraints:
- You must use C (standard library only, no external CSV parsing libraries) for the data processing step.
- The input CSV does NOT have a header row.
- You can assume timestamps are strictly increasing and temperatures are valid floats. 
- You can assume maximum row length (even with embedded newlines) won't exceed 1024 bytes.