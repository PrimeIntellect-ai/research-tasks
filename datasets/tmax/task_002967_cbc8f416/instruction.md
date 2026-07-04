You are a localization engineer managing translation strings for a web application. You have received a raw CSV export of new translations from your vendor, located at `/home/user/translations.csv`.

Currently, the team's existing bash pipeline silently drops rows containing embedded newlines, which causes missing translations in production. Your task is to build a robust, Bash-only pipeline (using standard GNU coreutils like `awk`, `sed`, `grep`, etc.) to process this CSV, sanitize it, mask PII, and generate a bulk SQL import script.

Write a bash script at `/home/user/process_locales.sh` that orchestrates this pipeline. When executed, your script must read `/home/user/translations.csv` and produce a SQL file at `/home/user/bulk_import.sql`.

The pipeline must perform the following transformations:
1. **Handle Embedded Newlines:** The `translation` column (column 3) often contains text enclosed in double quotes with embedded newline characters. Your script must convert these actual newline characters *within* the quoted fields into the literal two-character string `\n`, so each CSV record occupies exactly one line. (Assume quotes are only used to enclose fields with newlines or commas, and there are no escaped quotes `""` inside fields).
2. **Data Masking (PII):** The `translator_email` (column 4) contains personal information. You must mask the local part of the email address (before the `@`). Keep the first letter of the email, replace the rest of the local part with exactly three asterisks (`***`), and keep the domain intact. For example, `alice.smith@example.com` becomes `a***@example.com`.
3. **Bulk SQL Export:** Convert the cleaned, masked records (skipping the CSV header) into SQL `INSERT` statements. 
   - The table name is `locales`.
   - The columns are `id`, `lang`, `txt`, `email`.
   - Any single quotes (`'`) inside the translation text must be escaped by doubling them (`''`).
   - The generated SQL file should look exactly like this for each row:
     `INSERT INTO locales (id, lang, txt, email) VALUES ('<column1>', '<column2>', '<column3>', '<column4>');`

*Constraints:*
- Do not use Python, Perl, or Node.js. You must use shell built-ins and standard POSIX/GNU utilities (like `awk`, `sed`, `bash`).
- The CSV columns are strictly: `string_id,locale,translation,translator_email`.
- Make sure your script is executable and run it to produce the final `bulk_import.sql`.