You are acting as a data engineer helping a data scientist clean a messy dataset. We have a CSV file containing user feedback that our standard pipeline is failing to process because it silently drops rows with embedded newlines and chokes on invalid character encodings.

Your task is to write a C program that reads this dataset, cleans and anonymizes the data, and generates monthly Markdown reports.

**Input Data:**
Location: `/home/user/feedback.csv`
Format: `timestamp,email,"feedback_text"`
- `timestamp` is in ISO8601 format (e.g., `2023-10-15T14:30:00Z`).
- `email` is a standard email string.
- `"feedback_text"` is always enclosed in double quotes. It may contain embedded newlines and mixed/invalid non-ASCII byte sequences.

**Requirements for the C Program:**
1. **CSV Parsing**: Write a C program to read `/home/user/feedback.csv`. You must properly handle embedded newlines within the double-quoted `feedback_text`.
2. **Data Masking (Anonymization)**: Anonymize the email address. Keep the first letter, replace all remaining characters before the `@` with exactly three asterisks `***`, and keep the domain intact. (e.g., `alice@example.com` becomes `a***@example.com`, `bob@test.org` becomes `b***@test.org`).
3. **Character Encoding Handling**: Sanitize `feedback_text` by replacing any non-ASCII byte (byte value > 127) with a question mark `?`. Embedded newlines (`\n`) within the quotes should be preserved as literal newlines in the string.
4. **Time-based Bucketing & Template Generation**: For each record, extract the year and month (YYYY-MM) from the timestamp. Append the processed record to a Markdown file named `/home/user/reports/report_YYYY-MM.md` (e.g., `report_2023-10.md`). Create the directory `/home/user/reports/` if it does not exist.

**Output Template:**
For each parsed row, append the following exactly to the corresponding month's markdown file. Note the exact spacing and capitalization.

```markdown
## Feedback Entry
**Date:** <timestamp>
**User:** <masked_email>
**Comment:** <sanitized_feedback_text_without_surrounding_quotes>
---
```

**Execution:**
- Write your C code to `/home/user/clean_feedback.c`.
- Compile it to `/home/user/clean_feedback` using `gcc`.
- Run the compiled executable.
- Do not use external libraries outside of the C standard library. 

Verify that the output files in `/home/user/reports/` are generated correctly according to the template.