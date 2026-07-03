You are acting as a localization engineer. We have a telemetry stream containing latency metrics and localized error messages from various regions. The data is currently a messy CSV file with mixed character encodings and precise timestamps that need to be grouped.

Your task is to write a C++ program that processes this data, computes rolling statistics, aligns timestamps, normalizes character encodings, and outputs a clean JSON Lines file.

**Input File:**
There is a CSV file located at `/home/user/telemetry.csv` with the following columns:
`Timestamp,Locale,Encoding,Latency_ms,Message`

Example row:
`2023-10-12T08:15:32Z,fr-FR,ISO-8859-1,120,Dfaillance` (where the message is encoded in ISO-8859-1)

**Requirements:**
Write a C++ program (save it to `/home/user/process_loc.cpp`) and compile/run it to produce the output file. You may install standard Ubuntu packages (like `nlohmann-json3-dev`) using `sudo apt-get` if needed, but you must handle the compilation and execution.

For each row in the CSV (processed in order):
1. **Timestamp alignment:** Parse the ISO 8601 `Timestamp` and truncate it to the start of the minute (e.g., `2023-10-12T08:15:32Z` becomes `2023-10-12T08:15:00Z`).
2. **Character encoding handling:** Read the `Encoding` column. It will be either `UTF-8` or `ISO-8859-1`. If it is `ISO-8859-1`, you must convert the `Message` string into valid `UTF-8`. If it's already `UTF-8`, leave it as is.
3. **Rolling statistics computation:** Compute the rolling average of `Latency_ms` for the specific `Locale` based on the last **3** events (including the current one) for that locale. If a locale has fewer than 3 events so far, average the available events.
4. **Output format:** Write a JSON Lines file to `/home/user/processed_locales.jsonl`. Each line must be a valid JSON object representing one row from the input, in the exact same order.

The output JSON object must have these exact keys:
* `"aligned_time"`: The truncated timestamp string (e.g., `"2023-10-12T08:15:00Z"`).
* `"locale"`: The locale string (e.g., `"fr-FR"`).
* `"rolling_avg_latency"`: The computed rolling average as a float, rounded to exactly 2 decimal places (e.g., `120.00` or `125.33`).
* `"message_utf8"`: The UTF-8 normalized message.

**Constraints:**
- The CSV file does not have headers; the first row is data.
- Do not use quotes inside the CSV fields (assume simple comma separation).
- Compile with `-std=c++17` or higher.