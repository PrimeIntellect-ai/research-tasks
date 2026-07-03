You are a data analyst tasked with processing batches of user-submitted SQL queries in CSV format. Your company has recently implemented a set of strict database security rules to prevent unauthorized data access and denial-of-service attacks. 

Unfortunately, the DBA team only provided these rules as a screenshot of a memo, which is located at `/app/rules.png`.

Your task is to build an automated query sanitizer.
1. Inspect the image at `/app/rules.png` to extract the list of restricted tables and forbidden functions. (Tools like `tesseract-ocr` are available on the system).
2. Create an executable script at `/home/user/sanitizer.sh`.
3. The script must take a single command-line argument: the path to a CSV file.
4. The CSV file will have the header `query_id,query_text`. 
5. Your script must evaluate every `query_text` in the provided CSV file against the rules extracted from the image.
   - If **all** queries in the CSV are safe, the script must print exactly `ACCEPT` to standard output and exit.
   - If **any** query in the CSV references a restricted table or uses a forbidden function (case-insensitive), the script must print exactly `REJECT` to standard output and exit.

Make sure your script is robust against different casings in the SQL queries and correctly ignores the CSV header. Set the execute permission on your script once you are done. Do not hardcode the script to only work on specific test files; it will be evaluated against a hidden suite of clean and malicious CSV batches.