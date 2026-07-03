You are a data engineer building a high-performance ETL pipeline for an IoT sensor network. We are receiving noisy, duplicated data from the edge, and we need a C-based processor to clean, normalize, aggregate, and format this data.

Your task is to write a C program at `/home/user/etl_processor.c`, compile it to `/home/user/etl_processor`, and run it to process an input file located at `/home/user/raw_data.csv`. The output should be written to `/home/user/summary.txt`.

**Input Data:**
The file `/home/user/raw_data.csv` contains lines with the following format:
`YYYY-MM-DDTHH:MM:SS,sensor_id_raw,value`
(e.g., `2023-10-15T14:23:01,alpha_sensor,10.5`)

**Requirements for the C Program:**

1. **Regex Parsing:** 
   Use POSIX `<regex.h>` to validate and parse each line. The strict regex pattern must be:
   `^([0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}),([a-zA-Z_]+),([0-9]+(\.[0-9]+)?)$`
   Any line failing to match this pattern should be silently dropped.

2. **Cleaning & Distance-based Normalization:**
   We only have three valid sensors in our network: `"alpha_sensor"`, `"beta_sensor"`, and `"gamma_sensor"`.
   Due to transmission noise, the `sensor_id_raw` might be misspelled. You must implement the **Levenshtein distance** algorithm in C. 
   For each parsed row, calculate the Levenshtein distance between the extracted sensor name and the three valid sensors. Map the row to the valid sensor with the lowest distance. 
   *Rule:* If the lowest distance is strictly greater than 2, drop the row entirely. (If there's a tie for lowest distance, you can pick the first one, but the test data will not have ambiguous ties).

3. **Deduplication:**
   If a row has the exact same timestamp, the exact same mapped valid sensor name, and the exact same value as the **immediately preceding** valid parsed row, it is a duplicate and must be dropped.

4. **Time-based Bucketing & Aggregation:**
   Group the cleaned, normalized, and deduplicated data by the hour. To do this, truncate the timestamp to the top of the hour (e.g., `2023-10-15T14:23:01` becomes `2023-10-15T14:00:00`).
   Calculate the average value for each sensor for each hour.

5. **Template-based Generation:**
   Output the aggregated data to `/home/user/summary.txt`.
   The output must be sorted chronologically by the bucketed hour string, and then alphabetically by sensor name.
   Each line must strictly match this template:
   `[{BUCKETED_HOUR}] {VALID_SENSOR_NAME} AVG:{AVERAGE_VALUE}`
   *Note:* The average value must be formatted to exactly 2 decimal places (e.g., `AVG:11.50`).

Ensure your program handles missing files gracefully and can be compiled using standard `gcc` without additional external libraries (POSIX and standard C libraries only). Compile with `gcc -o /home/user/etl_processor /home/user/etl_processor.c`. Run the program and ensure `/home/user/summary.txt` is generated.