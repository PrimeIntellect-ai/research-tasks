You are a data scientist tasked with cleaning a messy, pipe-delimited (`|`) dataset of user feedback. You must write a Bash script named `/home/user/clean_data.sh` that orchestrates a multi-stage data processing pipeline.

The raw input file is located at `/home/user/raw_feedback.txt`.
It has no header. The columns are: `id|email|timestamp|feedback`

Your pipeline must perform the following steps in order and output the final processed data to `/home/user/cleaned_feedback.txt` and a summary report to `/home/user/report.md`.

**Step 1: Hash-based Deduplication**
Filter out duplicate rows based on the `feedback` column. If multiple rows have the exact same `feedback` text (case-sensitive), keep only the *first* occurrence and discard the rest.

**Step 2: Data Masking and Anonymization**
Replace the `email` column with an anonymized version. To anonymize an email address (e.g., `user@example.com`):
1. Compute the MD5 hash of the *entire* original email address (do not include a trailing newline when hashing).
2. Take the first 8 characters of this MD5 hash.
3. Extract the domain part of the original email address (e.g., `example.com`).
4. Format the anonymized email as `<8-char-hash>@<domain>`.

**Step 3: Feature Extraction**
Append a new 5th column to the output data representing the `word_count` of the `feedback` text. Use standard word counting logic (equivalent to what `wc -w` would produce for the text in that column).

The final output file `/home/user/cleaned_feedback.txt` must be pipe-delimited (`|`) with the columns:
`id|anonymized_email|timestamp|feedback|word_count`

**Step 4: Template-based Report Generation**
Generate a markdown file at `/home/user/report.md` exactly matching this template format:
```markdown
# Data Cleaning Report
Original rows: <N>
Cleaned rows: <M>
```
Where `<N>` is the total number of lines in `raw_feedback.txt` and `<M>` is the total number of lines in `cleaned_feedback.txt`.

Execute your script to produce the output files.