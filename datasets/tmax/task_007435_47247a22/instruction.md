You are a data engineer building a high-performance ETL pipeline. 

We have a raw sensor feed in a JSON-lines format at `/home/user/data.jsonl`. However, the upstream system occasionally injects unicode escape sequences (like `\u00b0C` for °C) directly into the value strings, which has broken our standard parsers. Furthermore, the readings arrive at irregular intervals and sometimes contain multiple readings per minute, or skip minutes entirely.

Your task is to write a C program, saved at `/home/user/etl.c` and compiled to `/home/user/etl`, that performs the following data processing steps:

1. **Multi-format reading & Cleaning:** Parse the JSON-lines file. Extract the `time` string, and the `alpha` and `beta` sensor values. You must correctly parse the floating-point values from strings like `"10.5\u00b0C"`, discarding the unicode escapes and unit characters.
2. **Timestamp alignment & Deduplication:** Truncate (floor) each timestamp to the start of the minute (e.g., `2023-01-01T12:00:45Z` becomes `2023-01-01T12:00:00Z`). If multiple records fall into the same aligned minute, keep *only the first* record encountered for that minute.
3. **Resampling & Gap-filling:** Determine the overall minimum and maximum aligned minutes in the dataset. For any minutes that are completely missing between the min and max, perform a Forward Fill (use the `alpha` and `beta` values from the most recent available minute). 
4. **Reshaping:** Transform the data from wide format (`time`, `alpha`, `beta`) into a long format (`timestamp`, `sensor`, `value`).
5. **Output:** Write the results to `/home/user/output.csv`. The CSV must include a header line `timestamp,sensor,value`. Sort the file chronologically by timestamp. For rows with the same timestamp, sort alphabetically by sensor name (i.e., `alpha` before `beta`). Format the float values to exactly one decimal place.

**Input Format Example:**
```json
{"time":"2023-01-01T12:00:10Z","alpha":"10.0\u00b0C","beta":"12.0\u00b0C"}
```

Compile your code using `gcc /home/user/etl.c -o /home/user/etl` and execute it to generate the final `/home/user/output.csv`. You may use standard C libraries.