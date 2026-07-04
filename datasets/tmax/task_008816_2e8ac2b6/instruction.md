You are a localization engineer managing a pipeline for software translations. Your current JSON-lines parser keeps breaking on Unicode escape sequences in the incoming translation logs. You need to write a robust Bash-based ETL script to process these logs directly.

Your task is to create a Bash script that processes `/home/user/raw_translations.jsonl` and outputs the result to `/home/user/qa_sample.jsonl`.

The input file is a JSON-lines file where each line is a JSON object with the following schema:
`{"lang": "<language_code>", "seq_id": <integer>, "translator": "<email>", "text": "<translated_text>"}`

Your pipeline must perform the following operations:

1. **Data Masking and Anonymization**: Replace the `translator` field's value (the email) with its SHA-256 hash (lowercase hex string).
2. **Unicode Decoding**: The `text` field contains Unicode escape sequences (e.g., `\u00f3`). Convert all of these into their actual UTF-8 character equivalents.
3. **Resampling and Gap-Filling**: For each language (`lang`), the `seq_id` should be a continuous sequence from the minimum `seq_id` to the maximum `seq_id` present for that language. Find any missing `seq_id`s in that range and insert synthetic records for them. The synthetic records must have:
   - `lang`: the respective language code
   - `seq_id`: the missing integer ID
   - `translator`: exactly the string `"SYSTEM"`
   - `text`: exactly the string `"UNTRANSLATED"`
4. **Data Sampling and Stratification**: To prepare a Quality Assurance (QA) sample, extract exactly three records for *each* language from the gap-filled dataset:
   - The record with the minimum `seq_id`.
   - The record with the median `seq_id`. Calculate the median as `floor((min_seq_id + max_seq_id) / 2)`.
   - The record with the maximum `seq_id`.

**Output Format**:
Write the final sampled records to `/home/user/qa_sample.jsonl`. Each line must be a valid JSON object containing all four fields (`lang`, `seq_id`, `translator`, `text`). The file must be sorted alphabetically by `lang` first, and then numerically by `seq_id` ascending.

Write and execute the Bash code to perform this task. You may use standard Linux utilities available in most distributions (e.g., `jq`, `awk`, `sed`, `sha256sum`, `coreutils`).