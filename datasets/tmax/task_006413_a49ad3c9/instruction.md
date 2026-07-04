I need your help building a C-based ETL tool to process some messy IoT sensor data. I'm a data analyst, and our legacy sensors export a wide-format CSV file with URL-encoded strings and irregular timestamps. 

Please write a C program located at `/home/user/etl.c` that reads `/home/user/raw_data.csv` and outputs a reshaped, normalized CSV to `/home/user/processed_data.csv`.

Here are the requirements for the C program:
1. **Wide-to-Long Reshaping:** The input CSV has the header `Timestamp,Status,Temp,Humidity`. You need to unpivot this so each sensor reading (Temp and Humidity) gets its own row. The output header must be exactly `timestamp_aligned,metric_name,metric_value,status_normalized`.
2. **Timestamp Alignment:** The input timestamps look like `2023-10-12T08:14:32Z`. You must align (truncate) these to the start of the hour. For example, `2023-10-12T08:14:32Z` becomes `2023-10-12T08:00:00Z`.
3. **Encoding & Normalization:** The `Status` column contains URL-encoded strings (e.g., `System%20OK%21`). 
    - Decode the URL-encoded characters (convert `%XX` hex sequences to their ASCII equivalent).
    - Normalize the resulting string by converting all uppercase letters to lowercase.
    - Replace any space characters (` `) with underscores (`_`).
4. **Values:** The sensor values (`Temp` and `Humidity`) should be printed as floats with exactly one decimal place (`%.1f`). 
5. Skip the input header row, but ensure your output file includes the output header row as the first line.

Once you have written `/home/user/etl.c`, compile it using `gcc -O2 -Wall /home/user/etl.c -o /home/user/etl` and then execute it to generate `/home/user/processed_data.csv`.

Example Input (`raw_data.csv`):
```
Timestamp,Status,Temp,Humidity
2023-10-12T08:14:32Z,System%20OK,22.5,45.2
2023-10-12T09:05:01Z,Error%3A%20Low%20Batt,21.0,40.1
```

Example Expected Output (`processed_data.csv`):
```
timestamp_aligned,metric_name,metric_value,status_normalized
2023-10-12T08:00:00Z,Temp,22.5,system_ok
2023-10-12T08:00:00Z,Humidity,45.2,system_ok
2023-10-12T09:00:00Z,Temp,21.0,error:_low_batt
2023-10-12T09:00:00Z,Humidity,40.1,error:_low_batt
```

Ensure your C program robustly handles the data formatting and produces the exact output required.