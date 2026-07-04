You are a configuration manager tasked with tracking historical capacity changes for a critical database server. 

You have been provided with an unstructured log file located at `/home/user/raw_config_logs.txt`. This file contains configuration update events for various servers. However, some logging glitches caused the `max_memory` values to be recorded as `???` instead of the actual integers.

Your task is to write a Python script that processes this log file to extract, impute, and analyze the memory configuration changes for a specific server.

Follow these exact steps:
1. Parse `/home/user/raw_config_logs.txt` and extract all lines pertaining ONLY to the server `app-db-primary`.
2. Extract the ISO-8601 timestamp and the `max_memory` value from each matching line.
3. Sort the extracted records chronologically by timestamp (ascending).
4. For any `max_memory` values that are missing or represented as `???`, perform **index-based linear interpolation** to fill in the missing numeric values. (i.e., if row 0 is 1000 and row 2 is 1200, row 1 should be imputed as 1100.0). You may assume the first and last records for `app-db-primary` always have valid integer values.
5. Compute a **3-period rolling average** (simple moving average of the current row and the two preceding rows) of the imputed `max_memory` values. If fewer than 3 periods are available (e.g., the first and second rows), compute the average of whatever periods are available up to that point.
6. Round both the imputed `max_memory` and the `rolling_avg` to exactly 2 decimal places.
7. Save the final processed data as a CSV file at `/home/user/rolling_config_stats.csv` with exactly the following headers: `timestamp,max_memory,rolling_avg`.

Ensure your Python script creates the CSV file with the correct formatting. You can use standard data processing libraries like `pandas` if you wish (you may need to install them using pip).