You are a data scientist tasked with cleaning and normalizing a messy set of customer records. You have received three files in different formats and encodings, located in `/home/user/data/`. Your goal is to combine, clean, and normalize these records into a single CSV file using only Bash built-ins and standard Linux CLI tools (like `awk`, `sed`, `iconv`, `jq`, `sort`, `tr`, etc.). Do not use Python, Perl, or other scripting languages.

Input files:
1. `/home/user/data/part1.csv`: A comma-separated values file. The file is encoded in ISO-8859-1 (Latin-1).
2. `/home/user/data/part2.tsv`: A tab-separated values file. The file is encoded in UTF-8.
3. `/home/user/data/part3.json`: A JSON file containing an array of objects. The file is encoded in UTF-8. The keys are `id`, `fullName`, `contactEmail`, and `phoneNumber`.

Normalization Rules:
You must produce a single output file at `/home/user/normalized_customers.csv` with the header exactly as:
`id,name,email,phone`

For each record across all files, apply the following transformations:
1. **id**: Pad with leading zeros to make it exactly 6 digits (e.g., `12` becomes `000012`).
2. **name**: 
   - Ensure the text is properly encoded in UTF-8.
   - Strip leading and trailing whitespace.
   - Convert the entire string to UPPERCASE. (Assume a UTF-8 locale like `en_US.UTF-8` is available and should be used).
3. **email**: 
   - Strip leading and trailing whitespace.
   - Convert the entire string to lowercase.
4. **phone**:
   - Extract only the digits from the string.
   - If the resulting digit string starts with '1' and is exactly 11 digits long, remove the leading '1'.
   - If the final digit string is exactly 10 digits long, format it as `XXX-XXX-XXXX`.
   - If the final digit string is NOT exactly 10 digits long, output the exact string `INVALID`.

Final Output Requirements:
- The output file `/home/user/normalized_customers.csv` must be encoded in UTF-8.
- The file must contain the header row `id,name,email,phone`.
- The records must be sorted numerically by the `id` column in ascending order.
- Do not include the original header rows from the input CSV/TSV files in your data rows.

Example of expected row:
Input: `12, José PÉREZ ,  Jose@example.COM,(555) 123-4567` (in Latin-1)
Output: `000012,JOSÉ PÉREZ,jose@example.com,555-123-4567` (in UTF-8)