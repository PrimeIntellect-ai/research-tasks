As an automation specialist, you are tasked with creating a robust data processing workflow to clean and analyze mathematical equation logs. These logs are exported from an OCR system into a CSV format, but they are notoriously messy: they contain multi-line notes (embedded newlines inside quoted CSV fields) which break naive line-by-line parsers.

Your objective is to build a pipeline that reads `/home/user/equations.csv`, processes the data, and writes the results to `/home/user/processed_equations.json`. You may use any programming language available in a standard Linux environment (e.g., Python, Node.js, bash tools, etc.).

Here are the strict processing rules:

1. **Robust CSV Parsing:** Read the file `/home/user/equations.csv`. The file has a header: `id,timestamp,equation,notes`. The `notes` column frequently contains embedded newline characters within quotes. You must parse the CSV correctly without silently dropping or misaligning these rows.
2. **Tokenization & Normalization:** For each row, extract the `equation` string and apply the following normalizations in this exact order:
    - Strip all whitespace characters (spaces, tabs, newlines) from the equation.
    - Replace all lowercase `x` characters with the multiplication asterisk `*`.
    - Replace all double asterisks `**` with a caret `^`.
3. **Hash-Based Deduplication:** Some equations are semantically identical after normalization. Compute the lowercase SHA-256 hex digest of the *normalized* equation. If you encounter a SHA-256 hash that has already been seen in an earlier row (based on the chronological order of the CSV), drop the current row completely.
4. **Windowed Aggregation:** For the remaining deduplicated rows (sorted by `timestamp` ascending), calculate the string length (number of characters) of the normalized equation. Then, compute a rolling moving average of these lengths using a window size of 3. This means the average should include the current row's length and up to 2 preceding deduplicated rows' lengths. 
5. **Output Formatting:** Write the final processed data to `/home/user/processed_equations.json` as a JSON array of objects. Each object must have the following keys:
    - `id` (integer): The original row ID.
    - `normalized` (string): The normalized equation.
    - `hash` (string): The SHA-256 hex digest of the normalized equation.
    - `rolling_avg_len` (float): The rolling average length, rounded to exactly 2 decimal places (e.g., 4.50, 3.33).

Ensure your script handles the entire workflow efficiently and gracefully.