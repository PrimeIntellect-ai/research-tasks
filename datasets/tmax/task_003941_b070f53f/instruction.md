You are a localization engineer managing translation strings for a global application. Our ETL job that ingests new translations occasionally fails and retries, resulting in duplicate records. Additionally, our lead translator just left an audio memo with urgent translation updates that need to be merged into the system.

Your task is to build a robust C-based translation serving pipeline.

1. **Audio Transcription**: 
   There is an audio file at `/app/loc_updates.wav`. It contains the lead translator dictating a few urgent translation updates. Transcribe it. The spoken format will be clear, specifying a timestamp, a language code, a translation key, and the translated string.

2. **Data Processing & Reshaping**:
   You have a historical dataset at `/home/user/historical.csv` in a long format: `timestamp,language,key,value`.
   Because of ETL retries, there are duplicate entries for the same `language` and `key` combinations.
   - Deduplicate the records by keeping only the row with the most recent `timestamp` for each `(language, key)` pair.
   - Combine these historical records with the new updates from the audio file. The audio updates should be treated as having the highest priority/latest timestamp.
   - Reshape the resulting dataset from the long format into a wide format CSV where each row represents a unique `key`, and the columns represent the languages (e.g., `key,en,es,fr`). If a translation is missing for a language, leave it blank. Save this parsed and reshaped CSV to `/home/user/translations_wide.csv`.

3. **HTTP Server (C)**:
   Write a C program (save as `/home/user/server.c` and compile to `/home/user/server`) that runs an HTTP server listening on `127.0.0.1:8080`.
   - When the server receives a `GET /translations` request, it must read `/home/user/translations_wide.csv` and return its contents with a `200 OK` status and `Content-Type: text/csv`.
   - Start this server in the background so it remains running.

4. **Pipeline Scheduling**:
   Create a cron job for the current user that runs at the top of every hour (e.g., `0 * * * *`) to copy `/home/user/translations_wide.csv` to `/home/user/backups/translations_wide_$(date +\%Y\%m\%d\%H\%M).csv`. Create the `/home/user/backups/` directory if it does not exist.

Ensure the server is running on port 8080 when you finish, and the cron job is installed.