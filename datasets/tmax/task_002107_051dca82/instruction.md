You are a data analyst operating entirely in a Linux terminal. You have been provided a messy server log file at `/home/user/server_metrics.csv`.

Your goal is to perform data schema enforcement, outlier removal, text tokenization, and correlation analysis using strictly Bash and standard command-line utilities (like `awk`, `grep`, `sed`, `tr`, `sort`, `bc`). Python or other high-level scripting languages are NOT allowed.

The CSV file has a header and should strictly follow this schema:
`id,cpu_usage,memory_usage,status_msg`

Perform the following steps:

1. **Schema Enforcement and Outlier Handling**:
   Filter `/home/user/server_metrics.csv` to create a cleaned file at `/home/user/clean_data.csv`. 
   A row is only valid if:
   - It contains exactly 4 comma-separated columns.
   - The `cpu_usage` and `memory_usage` columns are not empty.
   - The `cpu_usage` and `memory_usage` values are numeric and fall within the inclusive range of `0` to `100`.
   - Keep the original header in `clean_data.csv`.

2. **Tokenization**:
   Extract all text from the `status_msg` column of the *valid data rows* (excluding the header).
   - Extract only alphanumeric words (e.g., matching `[a-zA-Z0-9]+`).
   - Convert all words to lowercase.
   - Find the unique set of words.
   - Save these unique words to `/home/user/tokens.txt`, with exactly one word per line, sorted alphabetically.

3. **Correlation Analysis**:
   Calculate the Pearson correlation coefficient ($r$) between the `cpu_usage` and `memory_usage` columns using the valid rows in `clean_data.csv`. 
   - Calculate this using command-line tools (e.g., `awk`). 
   - Round the final correlation coefficient to exactly 4 decimal places.
   - Save the formatted output to `/home/user/correlation.txt`.

Ensure all output files are placed exactly at the specified paths.