You are a localization engineer analyzing logs of continuous translation updates. You have been given a CSV file containing translation activity logs at `/home/user/translation_logs.csv`. The file has the following header: `timestamp,lang,chars_translated`.

Your task is to calculate a 3-event rolling average of the characters translated specifically for the `es-ES` (Spanish) language locale, while applying constraint-based validation to filter out anomalous data.

Perform the following steps using standard bash tools (like `awk`, `grep`, `sed`, etc.):
1. Read `/home/user/translation_logs.csv`.
2. Filter the data to only include rows where `lang` is exactly `es-ES`.
3. Validate the `chars_translated` field: silently ignore any row where the value is less than 1 or greater than 5000 (which indicates a tool glitch or bot spam).
4. For the valid `es-ES` events, calculate a rolling (moving) average of the `chars_translated` over a window of exactly 3 valid events. 
5. Output the rolling average only when you have accumulated at least 3 valid events (i.e., start outputting from the 3rd valid event).
6. Format the output averages to exactly 1 decimal place.
7. Save the resulting averages, one per line, to `/home/user/rolling_es.txt`.

Example:
If the valid `es-ES` character counts in order are `100`, `200`, `150`, `310`, your output should be:
150.0
220.0

Please generate the required output file `/home/user/rolling_es.txt`.