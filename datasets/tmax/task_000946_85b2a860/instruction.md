You are a localization engineer managing the translation pipeline for a global software product. We are migrating our ETL pipeline to a new infrastructure, and you need to build the Bash-based orchestration and sanitization scripts.

We have a proprietary legacy translation compiler located at `/app/i18n_compiler`. It takes a CSV file containing translations and compiles it into a binary format used by our application. However, this binary is fragile: it crashes if translation strings contain mismatched template variables (e.g., `{userName}` in source but `{user_name}` in target), and it has no built-in protection against cross-site scripting (XSS) payloads injected by compromised translation vendors. 

Your task is to create a robust, multi-stage Bash pipeline that normalizes the incoming data, sanitizes it to drop invalid or malicious entries, and finally compiles it.

**Requirements:**
1. Write a sanitization script at `/home/user/sanitize_loc.sh`.
   - **Usage:** `bash /home/user/sanitize_loc.sh <input.csv> <output.csv>`
   - **Normalization:** Incoming CSVs might have Windows (`CRLF`) line endings. The output must have standard Unix (`LF`) line endings.
   - **Format:** The CSV has exactly 3 columns: `Key,Source,Target`. The header must always be preserved in the output.
   - **Validation (Variables):** Extract all variables enclosed in curly braces (e.g., `{count}`, `{userName}`). A row is **invalid** and must be dropped if the set of variable names found in the `Source` string does not exactly equal the set of variable names found in the `Target` string.
   - **Validation (Security):** A row is **invalid** and must be dropped if the `Target` string contains the substrings `<script>` or `javascript:` (case-insensitive).
   - Valid rows must be saved to the `<output.csv>`.

2. Write an orchestration script at `/home/user/process_all.sh`.
   - **Usage:** `bash /home/user/process_all.sh <input_directory> <output_directory>`
   - This script must find all `.csv` files in the `<input_directory>`.
   - For each CSV, it should run your `sanitize_loc.sh` to create a temporary clean CSV.
   - It must then pass the clean CSV to the legacy compiler: `/app/i18n_compiler <clean_input.csv> <output_directory>/<filename>.bin`. (Replace the `.csv` extension with `.bin`).

Ensure your Bash scripts are executable, use standard tools (e.g., `grep`, `awk`, `sed`, `tr`), and correctly handle edge cases in variable matching.