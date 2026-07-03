As a localization engineer, you are tracking the rendering performance of recently updated French (`fr_FR`) menu translations over time. You have a large, continuously growing stream of usage logs.

The logs are currently stored in `/home/user/loc_logs.csv` with the following format:
`timestamp,locale,translation_key,render_time_ms`
(e.g., `1700004500,fr_FR,menu_file_01,45`)

Your task is to write a memory-efficient C program that acts as a stream processor to extract specific time-series features for analysis. 

Requirements:
1. Write a C program at `/home/user/extract_ts.c`.
2. The program must read the CSV format from standard input (`stdin`) line by line to handle arbitrarily large files without loading everything into memory.
3. It must filter and transform the data based on the following rules:
   - **Locale Filter:** Only process lines where the locale is exactly `fr_FR`.
   - **Regex Match:** Use C's POSIX regex library (`<regex.h>`) to keep only lines where the `translation_key` perfectly matches the pattern `^menu_[a-z]+_[0-9]+$`.
   - **Time Series Aggregation Transform:** Floor the `timestamp` (which is a Unix epoch integer) to the nearest hour. (An hour is 3600 seconds. For example, 1700004500 becomes 1700001600).
   - **Feature Extraction:** Transform the `render_time_ms` (integer) into a categorical feature: output `FAST` if the time is strictly less than 100, and `SLOW` if it is 100 or greater.
4. Output the processed records to standard output (`stdout`) in the following format:
   `timestamp_hour,translation_key,performance_category`
   (e.g., `1700001600,menu_file_01,FAST`)

Once your C program is written:
1. Compile it to an executable named `/home/user/extract_ts` (e.g., using `gcc -O2`).
2. Stream the data through your program and save the output:
   `cat /home/user/loc_logs.csv | /home/user/extract_ts > /home/user/fr_menu_ts.csv`

Ensure your program handles missing fields gracefully and ignores malformed lines.