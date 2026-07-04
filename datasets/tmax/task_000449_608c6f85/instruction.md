You are a data analyst troubleshooting an ETL pipeline that failed midway and was retried, resulting in a messy data dump. 

Your objective is to write and execute a Python script to clean, deduplicate, and anonymize this data, and then generate a summary report.

**Input Data:**
There is a file located at `/home/user/data/raw_transactions.csv`. 
Because of a misconfiguration in the legacy system, this file is encoded in `ISO-8859-1`. It contains customer transaction records with the following columns: `transaction_id,customer_name,email,amount,notes`.
Due to the ETL retry, there are duplicate rows in this file.

**Requirements for your Python script:**
1. **Encoding & Reading:** Read the CSV file handling the `ISO-8859-1` encoding properly to preserve international characters (like é, ñ, ö).
2. **Deduplication:** Remove duplicate records based on the `transaction_id` column. If multiple rows have the same `transaction_id`, keep only the first occurrence.
3. **Data Masking:** Anonymize the `email` column to protect PII. The masking rule is: Keep the first character of the email's local part (the part before the `@`), replace the rest of the local part with exactly three asterisks `***`, and leave the `@` and the domain intact. 
   *(Example: `john.doe@example.com` becomes `j***@example.com`)*
4. **Output Data:** Save the cleaned, deduplicated, and anonymized data to a new CSV file at `/home/user/data/clean_transactions.csv`. This new file **must** be encoded in `UTF-8` and include the same headers.
5. **Template Summary:** Generate a summary report and save it to `/home/user/data/summary.txt` using exactly this format:
   ```
   ETL Run Summary
   Raw records: {raw_count}
   Unique records: {unique_count}
   Duplicates removed: {dupe_count}
   ```
   *(Replace the `{}` placeholders with the actual integer counts. The header row should NOT be counted as a record).*

Write the script, run it, and ensure all output files are correctly generated in `/home/user/data/`.