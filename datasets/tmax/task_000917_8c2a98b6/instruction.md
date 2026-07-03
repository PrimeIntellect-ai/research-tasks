You are a localization engineer managing translation strings for a global application. A flaky ETL job that imports daily translation dumps has a known bug: when it retries after a timeout, it produces duplicate records. Furthermore, upstream systems sometimes inject invalid data.

Your task is to write a Bash script at `/home/user/process_translations.sh` that cleans, validates, and deduplicates the raw translation dump, acting as a strict quality gate before the data is merged into the main application.

The raw dump is located at `/home/user/raw_translations.csv`. It has no header. 
The columns (comma-separated) are:
1. `TranslationKey` (string)
2. `Locale` (string)
3. `TranslatedText` (string)
4. `Timestamp` (integer, Unix epoch)
5. `State` (string)

Your script must perform the following pipeline in order:

**1. Constraint-Based Data Validation**
Filter out any row that violates *any* of the following constraints:
*   `Locale` must strictly follow the format of two lowercase letters, a hyphen, and two uppercase letters (e.g., `en-US`, `fr-FR`).
*   `TranslatedText` must not be empty.
*   `State` must be exactly either `APPROVED` or `DRAFT`.

**2. Deduplication (Sorting & Grouping)**
Because of the ETL retry bug, there may be multiple rows with the same `TranslationKey` and `Locale`.
*   Group the valid rows by `TranslationKey` and `Locale`.
*   For each group, keep *only* the single record with the highest `Timestamp`.

**3. Output and Quality Gate**
*   Write the cleaned, valid, deduplicated records to `/home/user/clean_translations.csv` (same comma-separated format, no header). The order of the output rows does not matter.
*   Calculate the total number of strictly `APPROVED` records for the `en-US` locale in the *final cleaned dataset*.
*   Write this exact integer to `/home/user/gate_metrics.txt`.
*   **Quality Gate:** If the count of `APPROVED` `en-US` translations is less than 3, your script must exit with status code `1` (indicating a failed quality gate). Otherwise, it must exit with status code `0`.

Ensure the script is executable (`chmod +x /home/user/process_translations.sh`). Run your script so the output files are generated for verification.