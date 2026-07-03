You are a data analyst working with an ETL pipeline. An upstream job failed and retried automatically, causing duplicate records to be appended to the output file. You need to write a C++ program to clean, validate, reshape, and anonymize this data.

The raw data is located at `/home/user/raw_data.csv` and has the following wide-format header:
`record_id,email,Q1_score,Q2_score,Q3_score,Q4_score,timestamp`

Write a C++ program at `/home/user/process.cpp`, compile it, and run it to produce a cleaned file at `/home/user/clean_data.csv` with the header:
`record_id,masked_email,quarter,score`

Your C++ program must implement the following logic:
1. **Deduplication (Validation):** Due to ETL retries, there are duplicate `record_id`s. Group by `record_id` and keep *only* the data from the row with the highest `timestamp`.
2. **Reshaping (Wide to Long):** Convert the wide record into up to four separate rows, one for each quarter. The `quarter` column should contain the string literal `Q1`, `Q2`, `Q3`, or `Q4`.
3. **Quality Gates:** Drop any reshaped row where the score is empty, strictly less than 0, or strictly greater than 100.
4. **Data Masking:** Anonymize the `email` field by keeping only the first character, replacing all remaining characters before the `@` symbol with exactly three asterisks (`***`), and keeping the domain intact. For example: `alice.smith@domain.com` becomes `a***@domain.com`.

**Output Requirements:**
- The output file `/home/user/clean_data.csv` must contain the header.
- The output rows must be sorted by `record_id` (ascending, numerically), and then by `quarter` (ascending, alphabetically).
- Write all necessary bash commands to compile and execute your program.