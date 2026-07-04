You are acting as a localization engineer managing translation quality across multiple time zones. You have exported a bulk time-series data file containing daily translation progress metrics from your database.

The file is located at `/home/user/loc_metrics.csv` and contains the following columns:
`timestamp,locale,strings_translated,errors_reported`

The file is sorted chronologically by `timestamp`.

Your task is to write a C program that processes this time-series data to find anomalous translation batches. 

Write your C code in `/home/user/process_metrics.c`, compile it, and run it. The program must perform the following:

1. **Tokenization and Parsing:** Read and parse the CSV. Skip the header row.
2. **Cleaning and Deduplication:** Due to an export glitch, there are duplicate entries. If you encounter consecutive rows with the exact same `timestamp` AND `locale`, you must process only the *first* instance and ignore the consecutive duplicates.
3. **Anomaly Detection:** Identify anomalous translation days. An anomaly is defined as any record where:
   - `strings_translated` is strictly greater than 100.
   - The error rate (calculated as `errors_reported` divided by `strings_translated` as a floating-point number) is strictly greater than `0.20` (20%).
4. **Export Validation Checkpoint:** The program must output the detected anomalies into a valid JSON file located at `/home/user/anomalies.json`. 

The JSON must be an array of objects, with each object formatted exactly like this (respecting the property names and outputting the `error_rate` to exactly two decimal places):
```json
[
  {
    "timestamp": 1700086400,
    "locale": "de-DE",
    "error_rate": 0.30
  }
]
```

Ensure your output is strictly valid JSON. Do not include any anomalies that don't meet both criteria.