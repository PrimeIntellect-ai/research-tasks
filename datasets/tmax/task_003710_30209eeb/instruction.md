You are a data analyst tasked with processing customer feedback data. You need to sanitize CSV files by masking Personally Identifiable Information (PII) before aggregating the data. 

You have been provided a proprietary internal library called `pii-masker` located at `/app/vendored/pii-masker`. However, the library is currently broken and failing tests. 

Your task consists of the following steps:

1. **Fix the Vendored Package**: 
   The `pii-masker` package has a deliberate perturbation in its source code (specifically in `pii_masker/rules.py` where a syntax error and a broken regex prevent it from compiling or correctly isolating SSNs). Fix the package so it can be installed via `pip install -e /app/vendored/pii-masker`. The fixed rules should correctly identify standard US SSNs (XXX-XX-XXXX) and standard email addresses, replacing them with `[SSN]` and `[EMAIL]` respectively.

2. **Develop the Sanitizer**:
   Write a Python script at `/home/user/sanitize.py` that accepts exactly two positional arguments: an input CSV file path and an output CSV file path.
   Usage: `python /home/user/sanitize.py <input_csv> <output_csv>`
   
   The script must:
   - Read the input CSV (which will have columns `user_id`, `date`, and `feedback`).
   - Deduplicate rows so that if multiple rows have the same `user_id`, only the first one (by order of appearance) is kept.
   - Use the fixed `pii-masker` library to sanitize the `feedback` column.
   - Write the cleaned, deduplicated data to the output CSV file, maintaining the original column order and headers.

3. **Verify Against Corpora**:
   There are two directories containing test datasets:
   - `/app/corpora/evil/`: Contains CSVs with real PII embedded in the feedback column. Your script MUST mask all PII here.
   - `/app/corpora/clean/`: Contains CSVs with text that looks similar to PII (e.g., 10-digit serial numbers like `123-45-67890`, or Twitter handles like `@company`) but contains NO actual PII. Your script MUST NOT alter the feedback text in these files.

Ensure your `sanitize.py` script is executable and strictly adheres to the input/output arguments. An automated grading script will iterate over both corpora and evaluate your script's output.