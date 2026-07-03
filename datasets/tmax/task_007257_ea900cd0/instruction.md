You are acting as a localization engineer. Our upstream ETL job that extracts translation strings from our content management system has a bug: when it encounters temporary network errors, it retries and produces duplicate records for the same translation keys in the output CSV. Furthermore, these duplicate records often contain partial data (e.g., one retry captures the Spanish translation, while another captures the Japanese translation). 

We need a multi-stage Go pipeline to clean, merge, reshape, and normalize this data. 

**Workspace Setup:**
Please work inside `/home/user/loc_pipeline/`.

**Input File:**
`/home/user/loc_pipeline/raw_translations.csv`
Columns: `timestamp,string_key,en,es,fr,ja,ar`
*Note: This file contains raw strings in various languages, including Arabic and Japanese, as well as emojis.*

**Task Requirements:**

Write a Go program (and any necessary shell commands to set up the module and run it) that processes the CSV file through the following pipeline stages:

1. **Deduplication and Gap-Filling (Resampling):**
   - Group the rows by `string_key`.
   - Sort the records for each `string_key` chronologically using the `timestamp` column (format: RFC3339, e.g., `2023-10-01T15:00:00Z`).
   - Merge the records to fill gaps: start with empty strings for all locales. Iterate through the sorted records for the key. If a locale has a non-empty string in a record, update the merged state for that locale. Newer records should overwrite older records *only if* the newer record has a non-empty value for that locale.

2. **Validation Checkpoint:**
   - After merging a key's records, check if the `en` (English) locale is empty. 
   - If `en` is empty, **drop** the entire `string_key` from the pipeline. It is invalid.

3. **Unicode Normalization:**
   - Normalize all resulting strings (keys and translations) to Unicode Normalization Form C (NFC). You must use the `golang.org/x/text/unicode/norm` package.

4. **Wide-to-Long Reshaping:**
   - Convert the merged, wide-format row (1 key -> up to 5 locales) into a long format. 
   - For every non-empty locale translation of a valid key, create an independent record.

5. **Output Generation:**
   - Output the long-format records as JSON Lines (JSONL) to `/home/user/loc_pipeline/normalized_translations.jsonl`.
   - Each line must be a JSON object with exactly three keys: `key`, `locale`, and `translation`.
   - Order of output lines does not matter.

**Example Input Row:**
`2023-10-01T10:00:00Z,greeting,Hello,,,こんにちは,`
`2023-10-01T11:00:00Z,greeting,,Hola,Bonjour,,مرحبا`

**Expected Output JSONL for the example (ignoring order):**
`{"key":"greeting","locale":"en","translation":"Hello"}`
`{"key":"greeting","locale":"es","translation":"Hola"}`
`{"key":"greeting","locale":"fr","translation":"Bonjour"}`
`{"key":"greeting","locale":"ja","translation":"こんにちは"}`
`{"key":"greeting","locale":"ar","translation":"مرحبا"}`