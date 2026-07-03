You are a localization engineer managing the UI string translations for a large software project. Recently, the UI rendering engine started generating binary telemetry data about the pixel widths of translated strings to help detect layout breakages.

Your task is to write a C program that reads this binary telemetry data, reshapes it, performs windowed aggregation to establish a baseline, detects layout anomalies, and logs the results to a CSV file.

**Input Data Specification:**
The telemetry data is located at `/home/user/telemetry.bin`. It is a raw binary file containing a sequence of fixed-size records (no headers, standard C struct packing/alignment for a 64-bit Linux system, little-endian). 
Each record corresponds to a specific UI string and contains 32-bit signed integers in the following order:
- `string_id`
- `en_width` (English width)
- `fr_width` (French width)
- `de_width` (German width)
- `es_width` (Spanish width)
- `ja_width` (Japanese width)

The records in the file are already sorted chronologically by `string_id`.

**Processing Requirements:**
You must write a C program (e.g., `process_telemetry.c`) that processes the file sequentially and does the following for each of the 4 target languages (`FR`, `DE`, `ES`, `JA`):

1. **Wide-to-Long Reshaping:** Conceptually process each language's metric individually for a given `string_id`.
2. **Windowed Aggregation:** For each language, maintain a sliding window of the widths of the **previous 4** strings processed. Calculate the integer average (mean) of these up to 4 previous widths. (Truncate the division towards zero, which is default C behavior for positive integers).
   - If fewer than 4 previous strings have been processed, average the available ones. 
   - If 0 previous strings have been processed, the average is considered `0`.
3. **Constraint Validation & Anomaly Detection:** An "Expansion Anomaly" occurs if a string meets **both** of the following conditions:
   - Constraint: The current translated width is strictly greater than `100` pixels.
   - Changepoint: The current translated width is strictly greater than `(previous_window_average * 3) / 2` (i.e., > 1.5x the rolling average).
4. **Window Update:** *After* checking for anomalies, add the current string's width to the sliding window for that language, pushing out the oldest value if the window already has 4 elements.

**Output Specification:**
Whenever an anomaly is detected, append a row to `/home/user/anomalies.csv`.
The CSV must have the following header line (exactly as written):
`string_id,language,current_width,rolling_avg`

For each anomaly, print the record in the format:
`[string_id],[language_code],[current_width],[rolling_avg]`
Where `[language_code]` is `FR`, `DE`, `ES`, or `JA`. 
If multiple languages trigger an anomaly for the same `string_id`, log them in the order: FR, DE, ES, JA.

**Constraints:**
- You must use C to process the data. Standard POSIX/C libraries are available.
- Compile your C code and run it to produce the final `/home/user/anomalies.csv`.
- Make sure to write the CSV headers even if no anomalies are found.