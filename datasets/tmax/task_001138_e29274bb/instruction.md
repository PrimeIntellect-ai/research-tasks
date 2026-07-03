You are a localization engineer managing translation strings for a software application. An automated ETL job exports translation updates from our database, but due to recent network retries, the export contains duplicate records for the same string IDs with different timestamps. Furthermore, some translation IDs haven't been translated yet and are completely missing from the export.

You have been provided with the raw export file at `/home/user/loc_exports.tsv`.
This file is tab-separated and contains the following columns:
1. `Timestamp` (Unix epoch time)
2. `MessageID` (Integer)
3. `Locale` (Language code, e.g., `es-ES`, `ja-JP`)
4. `Text` (UTF-8 translated string)

Your task is to create a clean, consolidated translation file specifically for the Spanish locale (`es-ES`) at `/home/user/es_final.tsv`. 

You must build a data processing pipeline using Bash tools (like `awk`, `sort`, `join`, etc.) that performs the following steps:
1. **Filter**: Extract only the records for the `es-ES` locale.
2. **Deduplicate**: If there are multiple entries for the same `MessageID`, keep *only* the entry with the most recent (highest) `Timestamp`.
3. **Gap Filling**: The application requires exactly 50 strings, with `MessageID`s running sequentially from `1` to `50`. Identify any missing `MessageID`s in the `1` to `50` range.
4. **Placeholder Insertion**: For every missing `MessageID`, insert a placeholder record. The placeholder text must be exactly `¡TRADUCCIÓN PENDIENTE!` (ensure proper UTF-8 handling).
5. **Format**: The final file `/home/user/es_final.tsv` must be a tab-separated file containing exactly 50 lines. It must contain only two columns: `MessageID` and `Text`, and it must be sorted in ascending numerical order by `MessageID`.

Do not include headers in the final output file.