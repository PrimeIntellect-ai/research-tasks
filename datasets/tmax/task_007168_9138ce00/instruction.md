You are a data engineer responsible for building an ETL pipeline to process financial transactions, detect anomalies, and prepare the data for downstream analysis while protecting PII (Personally Identifiable Information).

You need to write a Python script `/home/user/etl.py` that processes two raw datasets, transforms them, and writes the anomalous records to an output file. After writing the script, configure it to run as a scheduled cron job.

**Inputs:**
1. `/home/user/data/users.csv`: Contains user information.
   Columns: `user_id`, `name`, `email`, `ssn`
2. `/home/user/data/transactions.json`: Contains transaction logs. A JSON array of objects.
   Keys: `tx_id`, `user_id`, `amount`, `timestamp`, `description`

**Processing Requirements:**
1. **Join:** Merge the transactions with the user data based on `user_id`.
2. **Anonymization/Masking:**
   - Mask the `ssn` column so only the last 4 digits are visible, replacing everything else with 'X' (e.g., `123-45-6789` becomes `XXX-XX-6789`).
   - Mask the `email` column by keeping only the first character of the local part, replacing the rest of the local part with `***`, and keeping the domain intact (e.g., `alice.smith@example.com` becomes `a***@example.com`).
3. **Tokenization & Normalization:**
   - Normalize the `description` text by converting it to completely lowercase and removing all punctuation (only retain alphanumeric characters and spaces).
   - Tokenize the normalized description by splitting it on spaces into a list of words. Store this in a new field called `tokens`.
4. **Anomaly Detection:**
   - For each `user_id`, calculate the population mean and population standard deviation (ddof=0) of the `amount` field across all their transactions.
   - Flag a transaction as an anomaly if its `amount` is strictly greater than `mean + 1.5 * std_dev` for that user.

**Output:**
- The script should write the anomalous transactions to `/home/user/output/anomalies.jsonl` (one JSON object per line).
- Ensure the output directory exists.
- The JSON objects should contain exactly these keys: `tx_id`, `user_id`, `masked_ssn`, `masked_email`, `amount`, `tokens`. Do NOT include the original `ssn`, `email`, or `description`.

**Scheduling:**
- Create a cron job under the `user` account that runs `/home/user/etl.py` every 15 minutes.
- Save the crontab configuration you load into a file at `/home/user/crontab.bak`.