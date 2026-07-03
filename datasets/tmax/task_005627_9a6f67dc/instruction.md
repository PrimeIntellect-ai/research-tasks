You are a data scientist tasked with cleaning a large, corrupted JSON-Lines dataset of user feedback. The upstream data ingestion system has a bug that periodically produces invalid Unicode escape sequences (which breaks standard JSON parsers like `jq`), and it also leaks personally identifiable information (PII) in the form of email addresses.

Your task is to build a multi-stage data processing pipeline entirely in Bash (using standard tools like `sed`, `awk`, `jq`, `xargs`, `split`, etc.) to clean, validate, anonymize, and filter this dataset.

**Input Dataset:**
Path: `/home/user/raw_feedback.jsonl`

**Pipeline Requirements:**

1.  **Unicode Cleaning (Fixing Parsability):**
    The file contains invalid Unicode escape sequences that cause standard JSON parsers to fail. 
    You must find any sequence consisting of a literal `\u` followed by exactly 4 alphanumeric characters (`[A-Za-z0-9]{4}`) where at least one of those 4 characters is NOT a valid hexadecimal digit (`[0-9a-fA-F]`). 
    Replace the entire `\uXXXX` sequence with the literal string `[BAD_UNICODE]`. 
    (Valid unicode escapes like `\u0041` or `\u2605` must remain untouched).

2.  **Constraint-based Validation & Filtering:**
    After fixing the Unicode, parse the lines as JSON. You must drop any line that is NOT valid JSON.
    For valid JSON lines, keep ONLY the records where the `"category"` field is exactly equal to `"app_review"`. Drop all other records.

3.  **Data Masking / Anonymization:**
    Within the valid `"app_review"` records, look at the `"comment"` field (which is guaranteed to be a string). 
    You must find any email addresses in the `"comment"` field and replace them with `[REDACTED_EMAIL]`.
    For this task, an email address is strictly defined as matching the extended regular expression: `[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}`.

4.  **Parallel Execution:**
    Because the real dataset is large, your pipeline must process the data in parallel. 
    Write your main script at `/home/user/clean_pipeline.sh`. 
    The script must split the input file into chunks (e.g., using `split`), process those chunks in parallel (using `xargs -P` or background `&` jobs), and combine the results into a single output file. 

**Output:**
The final, cleaned, anonymized, and filtered JSON-Lines data must be saved to: `/home/user/clean_feedback.jsonl`. 
Make sure `/home/user/clean_pipeline.sh` is executable and run it to generate the final file.