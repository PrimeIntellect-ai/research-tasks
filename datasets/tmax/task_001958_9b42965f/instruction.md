You are a localization engineer managing an automated ETL pipeline that extracts translation strings from multiple sources. Recently, an ETL job failed midway and automatically retried. This retry resulted in duplicate, overlapping translation records across various file formats, and with misaligned timestamps. 

Your task is to write and execute a Python script that cleans, normalizes, deduplicates, and aggregates these translation records.

**Input Data:**
You will find three input files in `/home/user/loc_data/`:
1. `run1.json`: The initial JSON log containing extracted translations. The timestamp is a Unix epoch integer.
2. `run2_retry.csv`: The CSV log from the retry. The timestamp is an ISO8601 string (e.g., `2023-10-12T08:30:00Z`).
3. `manual_fixes.xml`: An XML file containing manual overrides. The timestamp is a Unix epoch float or integer.

All files contain the equivalent of these logical fields: `source`, `target_lang`, `translation`, and `timestamp`. Note that the exact field names or structures vary by format (e.g., JSON has `"src"`, CSV has `"source_text"`, XML has `<source>`). You must inspect the files to map them correctly.

**Processing Requirements:**
1. **Normalization**: To accurately identify duplicates, you must normalize the source text. 
   - Apply Unicode NFKC normalization.
   - Convert to lowercase.
   - Strip leading and trailing whitespace.
2. **Timestamp Alignment**: Convert all timestamps into standard Unix epoch time (integer or float). 
3. **Deduplication**: A record is considered a duplicate if the *normalized source text* and the *target language* are identical. When resolving duplicates, you must keep the record with the **most recent (highest) timestamp**. If timestamps are exactly equal, you can keep any.
4. **Aggregation**: Calculate the total number of unique valid translations per target language.

**Outputs:**
Your script must produce two output files in `/home/user/`:

1. `/home/user/cleaned_translations.json`:
   A JSON array of objects representing the final deduplicated records. Each object must have these exact keys: `normalized_source`, `target_lang`, `translation`, and `epoch_timestamp`.
   The array must be sorted alphabetically by `target_lang`, and then alphabetically by `normalized_source`.
   Format with 4-space indentation.

2. `/home/user/loc_stats.txt`:
   A text file containing summary statistics. Each line should be formatted as `target_lang: count` (e.g., `es: 42`), sorted alphabetically by `target_lang`.

You may use standard Python libraries, as well as `pandas` or `lxml`. If you need third-party packages, install them via `pip`.