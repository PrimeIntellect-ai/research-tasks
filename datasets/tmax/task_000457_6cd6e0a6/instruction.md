You are a data scientist preparing a customer review dataset for bulk import into a new analytics database. The raw data extraction produced a poorly formatted CSV file that needs cleaning, anonymization, and feature engineering using only standard Bash/Linux CLI tools (e.g., `awk`, `sed`, `grep`, standard coreutils).

The raw input file is located at: `/home/user/raw_reviews.csv`
It has a header and four columns: `id,email,rating,comment`

Write a Bash script or one-liner pipeline that processes this file and outputs the result to: `/home/user/import_ready.tsv`

Your pipeline must perform the following operations in a single multi-stage orchestration:

1. **Newline Record Dropping:** The extracting system occasionally included literal embedded newlines within the quoted `comment` field. Your pipeline must **silently drop** any logical record (CSV row) that spans multiple lines. Only records that are fully contained on a single line should be kept. Assume double quotes (`"`) are used for quoting. If a line has an odd number of quotes, it means a field continues to the next line; the entire multi-line record must be discarded.
2. **Data Masking (Anonymization):** The `email` column contains sensitive customer email addresses. You must replace the entire email address with the literal string `[REDACTED]` for all valid data rows.
3. **Rolling Statistics (Cumulative Sum):** You must add a fifth column named `cum_rating` representing the cumulative sum of the `rating` column up to that point, for all kept records.
4. **Format Conversion:** The output must be a Tab-Separated Values (TSV) file.

**Requirements:**
- The first line of `/home/user/import_ready.tsv` must be the header: `id	email	rating	comment	cum_rating` (tab-separated).
- Do not use Python, Perl, or any external scripting languages; stick strictly to standard Bash shell tools like `awk`, `sed`, `tr`, etc.
- Make sure you process the records sequentially to calculate the correct cumulative rating.

Example logic:
If `raw_reviews.csv` contains:
```
id,email,rating,comment
1,alice@domain.com,4,Nice
2,bob@domain.com,2,"Bad
service"
3,charlie@domain.com,5,Great
```
The output `import_ready.tsv` should be:
```
id	email	rating	comment	cum_rating
1	[REDACTED]	4	Nice	4
3	[REDACTED]	5	Great	9
```