You are a data analyst tasked with processing a daily batch of financial transactions. You must create a bash-only pipeline (using tools like `awk`, `sed`, `sort`, etc.) to process, validate, anonymize, and aggregate this data.

The raw data is located at `/home/user/raw_tx.csv`. 
It has a header and the following columns: `tx_id,name,email,amount,currency,date`

You need to perform the following steps and save your script as `/home/user/process.sh`. You should also execute the script to generate the final output files.

1. **Validation Checkpoint**:
   - Filter out any rows where the `amount` is less than or equal to 0.
   - Filter out any rows where the `currency` is NOT one of: `USD`, `EUR`, `GBP`.
   - Invalid rows should be appended to `/home/user/invalid_rows.log` (keep the original CSV format for these rows).

2. **Data Masking / Anonymization**:
   - For valid rows, mask the `name` column. Replace the entire name with the first character, three asterisks, and the last character. (e.g., "Alice Smith" -> "A***h").
   - Mask the `email` column. Keep the first character, add three asterisks, and keep the `@domain.com` part (e.g., "alice@example.com" -> "a***@example.com").

3. **Mathematical Processing**:
   - Convert all valid amounts to USD using the following fixed exchange rates:
     - USD: 1.00
     - EUR: 1.08
     - GBP: 1.25
   - Calculate the converted amount to 2 decimal places.

4. **Aggregation and Sorting**:
   - Group the valid transactions by the masked `email`.
   - Sum the total converted USD amounts for each masked email.
   - Sort the aggregated results in descending order based on the total USD amount.

5. **Multi-format Output**:
   - Write the aggregated, sorted results to `/home/user/summary.tsv` (Tab-Separated Values). The columns must be: `masked_email` [tab] `total_usd_amount`. No header.
   - Write a pipeline log to `/home/user/pipeline.log` with exactly this format on a single line:
     `[INFO] Processed <X> valid records, dropped <Y> invalid records.` (where `<X>` and `<Y>` are the respective counts).

Ensure your script handles everything correctly and produces the exact output files requested. Run your pipeline before finishing.