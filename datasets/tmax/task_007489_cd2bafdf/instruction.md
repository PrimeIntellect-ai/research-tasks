You are an automation specialist tasked with creating a robust Bash workflow to process, normalize, and anonymize raw customer feedback logs. 

You need to write a Bash script located at `/home/user/anonymize.sh`. The script must accept two arguments: the input file path and the output file path.
Usage: `/home/user/anonymize.sh <input_file> <output_file>`

The script must perform the following operations strictly using Bash shell built-ins and standard coreutils (like `sed`, `awk`, `grep`, `tr`, `sort`, `uniq`):

1. **Normalization & Cleaning:**
   - Convert all text to lowercase.
   - Trim all leading and trailing whitespace from every line.
   - Remove any lines that are empty (after trimming).

2. **Data Masking & Anonymization (Regex):**
   - **Emails:** Replace any email address with the exact string `[email]`. An email is defined as one or more alphanumeric characters, dots (`.`), underscores (`_`), hyphens (`-`), or pluses (`+`), followed by an `@` symbol, followed by one or more alphanumeric characters or hyphens, a dot (`.`), and two or more alphabetic characters.
   - **Phone Numbers:** Replace any US-style phone number with the exact string `[phone]`. You must match exactly two formats: 
     - `XXX-XXX-XXXX` (e.g., `123-456-7890`)
     - `(XXX) XXX-XXXX` (e.g., `(123) 456-7890`)
     *(Note: X represents a digit 0-9).*

3. **Deduplication:**
   - After all cleaning and masking, remove duplicate lines.
   - The final output written to the `<output_file>` must be sorted alphabetically.

Make sure the script is executable (`chmod +x /home/user/anonymize.sh`). You do not need to create the input file; assume it will be passed to your script. Ensure your regex patterns are robust and handle multiple occurrences of PII on the same line.