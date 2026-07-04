As an automation specialist, you are tasked with fixing and completing an ETL workflow that processes incoming transaction records. The upstream system frequently retries failed jobs, resulting in duplicated records, missing fields, and unmasked PII.

You need to perform two tasks: fix a broken vendored dependency, and write a deterministic Python pipeline script to clean the data.

### Step 1: Fix the Vendored Package
The pipeline relies on `python-dateutil`, which has been vendored at `/app/vendor/python-dateutil`. However, a recent internal patch broke it. 
1. Identify and fix the deliberate syntax/import error in the vendored `dateutil/parser/_parser.py` file.
2. Install the fixed package into your environment so your scripts can use it.

### Step 2: Implement the ETL Processor
Create a Python script at `/home/user/process_etl.py`. 
The script must read a JSON array of objects from `stdin` and output a processed JSON array to `stdout`.

Each input object will have the following schema:
- `id`: integer
- `email`: string
- `amount`: float or null
- `date_str`: string (various date formats)

Implement the following logic in exact order:

1. **Parsing & Sorting**: 
   - Parse `date_str` using `dateutil.parser.parse`. 
   - Sort the array of records chronologically (oldest to newest). If two records have the identical parsed datetime, preserve their original relative order from the input.

2. **Deduplication**: 
   - Iterate through the sorted records. If multiple records have the same `id`, keep only the **first** occurrence (the oldest one). Discard the rest.

3. **Imputation (Interpolation)**: 
   - For records where `amount` is `null`, impute the value by taking the arithmetic mean of the immediately preceding and succeeding valid (non-null) `amount` values in the deduplicated sequence.
   - If the `null` value is at the very beginning, use the first valid `amount` that follows it.
   - If the `null` value is at the very end, use the last valid `amount` that precedes it.
   - If all records have `null` amounts, set them all to `0.0`.
   - Round imputed amounts to 2 decimal places.

4. **Masking (Anonymization)**: 
   - Mask the `email` field to protect PII. Keep the very first character of the local part, replace the rest of the local part with exactly five asterisks (`*****`), and keep the `@` and domain intact. 
   - Example: `john.doe@example.com` becomes `j*****@example.com`.

5. **Deterministic Sampling (Stratification proxy)**: 
   - To reduce downstream load, filter the records to only include those where `id % 2 == 0` (even IDs).

Output the final list of dictionaries as a valid JSON array to `stdout` with no extra formatting (e.g., `json.dumps(data, separators=(',', ':'))`).

Ensure your script handles edge cases (e.g., empty arrays) gracefully by outputting `[]`. 
The verifier will execute your script with a large number of randomly generated JSON inputs and strictly compare your output bit-for-bit against a reference implementation.