You are a localization engineer managing an ETL pipeline that processes daily translation updates. The pipeline extracts logs from upstream services, but due to retry mechanisms, it often produces duplicate records (same timestamp, language code, and text). You need to clean this time-series data and produce summary statistics.

We have a skeleton C program at `/app/src/loc_aggregator.c` that is supposed to read `/app/data/loc_updates.csv`. You must complete this C program to perform the following:
1. **Read and parse** the CSV file. The columns are `timestamp` (ISO 8601, e.g., `2023-10-25T14:30:00Z`), `lang_code`, and `text`.
2. **Regex Validation**: Use `pcre2` to ensure `lang_code` strictly matches the pattern `^[a-z]{2}-[A-Z]{2}$` (e.g., `en-US`, `fr-FR`). Drop rows with invalid codes.
3. **Encoding Validation**: Ensure the `text` field contains strictly valid UTF-8. Drop rows with invalid UTF-8 byte sequences.
4. **Deduplication**: Due to ETL retries, exact duplicate rows (identical timestamp, lang_code, and text) may appear consecutively or within the same day. Count each unique update only once. 
5. **Aggregation**: Compute the number of valid, unique translation updates per day, per language code.
6. **Output**: Write the summary statistics to `/app/output/summary.csv` with the header `date,lang_code,update_count` (e.g., `2023-10-25,en-US,42`). Sort the output chronologically, then alphabetically by language code.

**Dependencies:**
You must use the `pcre2` library for regex processing. The source code for `pcre2-10.42` is vendored at `/app/pcre2-10.42`. 
However, a recent incomplete localization patch introduced a compilation error in the vendored `pcre2` source. You must fix the compilation error in `/app/pcre2-10.42/src/pcre2_compile.c` (hint: look for a missing semicolon or stray characters around line 150-200), build, and install the library so your C program can link against `-lpcre2-8`.

Compile your final aggregator to `/app/bin/loc_aggregator` and run it. Your pipeline's accuracy will be graded based on how closely the update counts match the true expected counts.