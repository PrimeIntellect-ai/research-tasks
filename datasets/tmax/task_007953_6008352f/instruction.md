You are a localization engineer tasked with cleaning up a messy translation metadata dump. Recently, an ETL job responsible for syncing translation memory records failed midway and was retried. This resulted in duplicate records, mixed timestamp formats, and unnormalized translation confidence scores.

You need to write a C program that processes this raw data, deduplicates it, aligns the timestamps, normalizes the confidence scores, and outputs a clean CSV along with a processing log.

**Input Data**
A raw text file is located at `/home/user/loc_data/raw_translations.txt`.
Each line represents a localization record with fields separated by a pipe `|`:
`StringID|Timestamp|ConfidenceScore|Locale`

- `StringID`: A string identifier (e.g., `BTN_OK`). Max 50 characters.
- `Timestamp`: The time the translation was committed. This is in one of two formats:
  1. A UNIX epoch integer (e.g., `1672531200`).
  2. An ISO 8601-like string in the exact format `YYYY-MM-DDThh:mm:ssZ` (e.g., `2023-01-01T00:00:00Z`). Treat this as UTC.
- `ConfidenceScore`: A floating-point number representing translation confidence.
- `Locale`: The target language locale (e.g., `en-US`). Max 20 characters.

**Requirements for your C program:**
1. **Deduplication:** The ETL retry caused duplicate entries for the same `StringID` and `Locale` combination. You must group records by the composite key `(StringID, Locale)`. For each group, keep *only* the record with the most recent (latest) timestamp. If there's a tie in timestamps, keep the one that appears first in the file.
2. **Timestamp Alignment:** Convert all timestamps into standard UNIX epoch integers (time_t). 
3. **Normalization (Math):** After deduplication, find the minimum (`MIN_CONF`) and maximum (`MAX_CONF`) confidence scores across the *deduplicated* dataset. Normalize all deduplicated confidence scores using min-max scaling so they fall between 0.0000 and 1.0000. Formula: `Normalized = (Score - MIN_CONF) / (MAX_CONF - MIN_CONF)`. (Assume MAX_CONF > MIN_CONF for this dataset).
4. **Output CSV:** Write the deduplicated, normalized records to `/home/user/loc_data/processed.csv`.
   - The file must include a header: `StringID,Locale,UnixTimestamp,NormalizedConfidence`
   - Records must be sorted alphabetically by `StringID` (ascending). If `StringID`s are identical, sort alphabetically by `Locale` (ascending).
   - `NormalizedConfidence` should be formatted to exactly 4 decimal places (e.g., `0.5000`).
5. **Pipeline Logging:** Write a log file to `/home/user/loc_data/pipeline.log` with the following exact format:
   ```
   TOTAL_RAW: <total_lines_read_from_input>
   TOTAL_DEDUPLICATED: <total_unique_records_after_dedup>
   MIN_CONF: <minimum_confidence_formatted_to_2_decimal_places>
   MAX_CONF: <maximum_confidence_formatted_to_2_decimal_places>
   ```

**Execution**
Write your C program to `/home/user/process_loc.c`, compile it using `gcc`, and execute it to generate the required output files. You may use standard C libraries (`stdio.h`, `stdlib.h`, `string.h`, `time.h`, etc.).