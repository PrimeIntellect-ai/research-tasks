You are a localization engineer managing translation files. The application generates a log of strings that are missing translations in specific locales. 

Your task is to write a Go program at `/home/user/loc_updater.go` that processes this log, updates the existing translation files, and generates an aggregated summary.

**Inputs:**
1. A log file at `/home/user/missing_strings.log`. Each line represents a missing translation event with the format:
   `YYYY-MM-DD HH:MM:SS | <locale> | <key> | <default_text>`
2. Existing translation files in JSON format located in `/home/user/locales/`. For example, `/home/user/locales/es.json` and `/home/user/locales/fr.json`. They contain simple key-value string pairs.

**Requirements for the Go program:**
1. **Extraction & Update:** Parse `missing_strings.log`. For every missing string, update the corresponding `<locale>.json` file in the `/home/user/locales/` directory. Add the `<key>` with the `<default_text>` as its value. If the key already exists in the JSON file, do not overwrite it. If the JSON file does not exist, create it.
2. **Windowed Aggregation:** Calculate the number of missing translation occurrences per locale, per hour bucket. An hour bucket truncates the time to the nearest hour (e.g., `2023-10-01 14:23:10` becomes `2023-10-01 14:00`). Note: count *every* log line, even if it's a duplicate key.
3. **Multi-format Output:** 
   - Write the updated JSON back to the `/home/user/locales/` directory (pretty-printed with 2 spaces).
   - Write the windowed aggregation to a CSV file at `/home/user/hourly_summary.csv`. The CSV must have the header `locale,hour_bucket,count` and be sorted alphabetically by locale, then chronologically by hour_bucket.
4. **Logging:** Append a line to `/home/user/pipeline.log` for every locale updated in the format: `Updated locale: <locale>`.

Run your Go program to perform these tasks. No external libraries are needed; use the standard library.