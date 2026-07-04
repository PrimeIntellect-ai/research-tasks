You are acting as a localization engineer updating our translation data pipeline. 

Our current data ingestion script is failing because it silently drops or mangles rows in our CSV files that contain embedded newlines in the translated text. We need a robust C++ solution that can properly parse these CSV files, normalize the timestamps, and export the data to JSON Lines format (JSONL).

Write a C++ program at `/home/user/parser.cpp` that does the following:
1. Takes two command-line arguments: the input CSV file path and the output JSONL file path.
2. Reads the input CSV file. The CSV has the following headers: `id,timestamp,lang,text`.
3. Properly handles the `text` field, which is enclosed in double quotes (`"`) and may contain embedded commas and newlines.
4. Parses the `timestamp` field, which is currently in the format `YYYY/MM/DD-HH:MM:SS`, and converts it to ISO 8601 format: `YYYY-MM-DDTHH:MM:SSZ`.
5. Escapes newline characters in the `text` field as `\n` in the JSON output, and escapes any inner double quotes as `\"`.
6. Writes each row as a single JSON object on a new line in the output file. Example format: `{"id": "1", "timestamp": "2023-10-05T14:30:00Z", "lang": "es", "text": "Hola,\nmundo"}`

After writing the C++ code:
1. Compile it to an executable named `/home/user/parser` using `g++`.
2. Run your program using the input file `/home/user/locales.csv` and output to `/home/user/processed_locales.jsonl`.
3. We need this pipeline to run automatically. Create a bash script at `/home/user/setup_cron.sh` that, when executed, installs a cronjob for the current user. The cronjob must execute `/home/user/parser /home/user/locales.csv /home/user/processed_locales.jsonl` exactly at 2:30 AM every day. Execute this script so the cronjob is active.