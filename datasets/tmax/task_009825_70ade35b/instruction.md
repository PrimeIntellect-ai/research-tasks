You are acting as a data scientist. We have a massive, messy text dump of sensor logs from a legacy system. The file is located at `/home/user/raw_sensor_logs.txt`. 

Your objective is to process this file and create a clean, standardized JSON Lines (JSONL) file at `/home/user/clean_data.jsonl`. Because the real production files are terabytes in size, you must use a streaming or line-by-line processing approach (do not load the entire file into memory at once).

Here is an example of a raw log line:
`[2023/10/05-14:32:01] | SENSOR_ID: Alpha-99 | TEMP: 85.4F | NOTES: "Warning: High humidity! recalibration needed."`
`[2023/10/06-09:15:22] | SENSOR_ID: Beta-02 | TEMP: 42.1F | NOTES: "All systems nominal."`
`Invalid or corrupted line without proper delimiters...`

You need to perform the following data processing steps on each valid line:
1. **Extraction**: Identify valid lines. A valid line strictly follows the format `[YYYY/MM/DD-HH:MM:SS] | SENSOR_ID: <id> | TEMP: <val>F | NOTES: "<text>"`. Ignore any lines that do not match this structure.
2. **Standardization (Timestamp)**: Convert the extracted timestamp into strict ISO 8601 UTC format: `YYYY-MM-DDTHH:MM:SSZ`.
3. **Normalization (Temperature)**: The temperature is provided in Fahrenheit. Convert it to Celsius using the formula `C = (F - 32) * 5/9`. Round the final Celsius value to exactly 2 decimal places.
4. **Tokenization and Text Normalization (Notes)**: Extract the text inside the quotes of the `NOTES` field. Convert it to lowercase, remove all punctuation (keep only alphanumeric characters `a-z` and `0-9` and spaces), and split it into an array of tokens (words).

For each valid line, output a single JSON object on a new line in `/home/user/clean_data.jsonl` with the following schema:
```json
{
  "timestamp": "2023-10-05T14:32:01Z",
  "sensor_id": "Alpha-99",
  "temp_celsius": 29.67,
  "tokens": ["warning", "high", "humidity", "recalibration", "needed"]
}
```

Write a script in your preferred language to perform this task, execute it, and ensure the `/home/user/clean_data.jsonl` file is correctly formatted and complete.