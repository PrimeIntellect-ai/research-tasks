You are a Data Engineer building the initial extraction and transformation phase of an ETL pipeline for a legacy customer support system. 

The system periodically dumps support tickets into the directory `/home/user/tickets_raw`. These files are notoriously messy due to historical migrations between different OS environments and logging libraries.

Your objective is to write and execute a script (in any language you choose) that processes all `.txt` files in `/home/user/tickets_raw` and produces a single cleaned JSON Lines file at `/home/user/tickets_clean.jsonl`.

Here are the requirements for your ETL job:

1. **Character Encoding Normalization:** The input files are saved in a mix of encodings, including UTF-8, ISO-8859-1, and Windows-1252. You must correctly read them and ensure the final JSONL output is strictly valid UTF-8. Watch out for special characters like `ñ`, `é`, and curly quotes `”`.

2. **Regex Extraction:** Each file contains exactly one ticket, but the format is plain text with varying whitespace. You must extract the following fields using Regular Expressions:
   - `date`: Found in lines starting with `Date: ` or `Reported: ` (e.g., `Date: 2023-10-12`). Extract just the date string.
   - `email`: Found in lines starting with `User: ` or `Email: `.
   - `error_code`: Found in lines starting with `Error: ` followed by a code in brackets, e.g., `Error: [ERR_404]`. Extract just the string inside the brackets. Sometimes the brackets are empty: `Error: []`.
   - `message`: The rest of the file content after the line `Message:`. It may span multiple lines. Strip leading/trailing whitespace.

3. **Imputation:** 
   - If the `error_code` is empty (e.g., from `Error: []`) or the `Error:` line is missing completely, you must impute the error code based on the `message` content (case-insensitive):
     - If the message contains the word "timeout", impute `ERR_504`.
     - If the message contains the word "denied" or "forbidden", impute `ERR_403`.
     - If the message contains the word "crash" or "exception", impute `ERR_500`.
     - For all other missing error codes, impute `ERR_UNKNOWN`.

4. **Output Format:**
   The output must be a JSON Lines file (`/home/user/tickets_clean.jsonl`), where each line is a valid JSON object representing one ticket.
   Keys must be strictly: `"date"`, `"email"`, `"error_code"`, `"message"`, and `"filename"` (the base name of the text file, e.g., `ticket_1.txt`).

Write the script, install any dependencies you might need, and execute it to produce the final `/home/user/tickets_clean.jsonl` file.