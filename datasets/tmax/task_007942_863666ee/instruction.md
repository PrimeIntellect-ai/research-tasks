You are a localization engineer managing a pipeline of translated UI strings. 

You recently discovered a major bug in the existing Bash pipeline: the naive `while read` loop was silently dropping or corrupting translation rows that contained embedded newline characters inside the quotes.

Your task is to create a robust data processing script at `/home/user/process_l10n.sh` that reads an input CSV, processes the data, enforces constraints, detects anomalies, and outputs the results in specific formats.

**Input:**
A CSV file located at `/home/user/l10n_input.csv` with the following header:
`string_id,locale,translation,status`

**Processing Requirements:**
1. **Robust CSV Parsing:** You must properly parse the CSV, preserving embedded newlines inside the `translation` column.
2. **Constraint-based Validation:** Filter the dataset based on the `status` column. Only keep rows where the status is EXACTLY `approved` or `pending`. Any other status (or empty status) must be completely dropped from all outputs.
3. **Normalization:** Normalize the `locale` column so the language code is lowercase and the country code is uppercase, separated by a hyphen (e.g., `EN-us` becomes `en-US`, `fr-fr` becomes `fr-FR`).
4. **Tokenization & Feature Extraction:** Calculate the "word count" of the `translation` string. For this task, a "word" is defined strictly as any contiguous sequence of non-whitespace characters (i.e., splitting by standard whitespace: space, tab, or newline).
5. **Anomaly Detection:** Anomaly translations are defined as rows (after validation) where the word count is `0` OR strictly greater than `20`.

**Outputs:**
Your script must process the input and generate two files:

1. **`/home/user/valid_translations.jsonl`**
   A JSON Lines file containing ONLY the validated rows that are NOT anomalies.
   Each line must be a valid JSON object with exactly these keys:
   `{"id": "<string_id>", "locale": "<normalized_locale>", "word_count": <integer_word_count>}`

2. **`/home/user/anomalies.csv`**
   A CSV file containing the rows that passed constraint validation but were flagged as anomalies.
   This file must include the exact same header as the input CSV (`string_id,locale,translation,status`).
   The data rows must reflect the **normalized** `locale` and preserve the original quoted translations (including any embedded newlines).

**Execution:**
Your script `/home/user/process_l10n.sh` must be executable and capable of running successfully when invoked with no arguments. You may use Bash alongside standard tools available in a standard Linux environment (like `awk`, `python3`, `jq`, etc.) to achieve the CSV handling.