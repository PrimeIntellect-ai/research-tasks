You are helping me fix a data processing pipeline. We have an input CSV file at `/home/user/input.csv` that contains user feedback. 
However, our current shell-based pipeline is failing because:
1. It splits rows incorrectly when there are embedded newlines inside quoted fields (e.g., in the `Feedback` column).
2. The file is encoded in ISO-8859-1, but downstream systems expect UTF-8.
3. We need to perform stratified sampling: extract exactly the first 2 records for each unique `Department`.

Write a C program at `/home/user/process.c` that solves these issues. 
Your C program must:
1. Read `/home/user/input.csv`.
2. Parse the CSV correctly, honoring double quotes `"` so that embedded newlines within quotes do not start a new record.
3. Convert the character encoding from ISO-8859-1 to UTF-8.
4. Implement stratified sampling: output only the first 2 records encountered for each `Department`. (Include the header row in the output).
5. Write the resulting valid CSV to `/home/user/output.csv`.

Once you have written the code, compile it with `gcc -o /home/user/process /home/user/process.c` and run it to generate the `/home/user/output.csv`.