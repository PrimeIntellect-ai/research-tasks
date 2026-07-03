You are a data engineer tasked with cleaning up a messy ETL data drop using Rust. An upstream ETL job failed and retried, dumping duplicate records into our raw log file. You need to write a Rust application that processes this file, performs deduplication, masks sensitive data, calculates mathematical statistics, and generates a formatted report.

**Input Data**
A file will be located at `/home/user/raw_data.txt`. Each line contains a transaction record in the following format:
`TxID: <Alphanumeric> | User: <String> | Card: <16-digit number> | Amount: <Float>`

**Requirements:**
1. **Initialize a Rust Project:** Create a new Cargo binary project at `/home/user/etl_processor`.
2. **Regex Parsing:** Read `/home/user/raw_data.txt` and parse the fields using a regular expression.
3. **Deduplication:** The retry mechanism caused duplicate `TxID`s. You must only process the *first* occurrence of each `TxID`. Ignore any subsequent lines with a `TxID` you have already seen.
4. **Data Masking:** Anonymize the 16-digit `Card` number by replacing the middle 8 digits with asterisks (`*`). For example, `1234567812345678` becomes `1234********5678`.
5. **Rolling Statistics:** Compute a 3-item rolling average of the transaction `Amount` (in the order they appear after deduplication). 
   - For the 1st transaction, it's just the 1st amount.
   - For the 2nd transaction, it's the average of the 1st and 2nd amounts.
   - For the 3rd transaction and onwards, it's the average of the current amount and the previous 2 amounts.
6. **Normalization:** Calculate the Min-Max normalized value for each transaction's `Amount` based on the *entire* deduplicated dataset. 
   - Formula: `(Amount - Min_Amount) / (Max_Amount - Min_Amount)`
7. **Template Generation:** Write the results to `/home/user/clean_report.txt`. For each deduplicated transaction, append the following template (exactly as shown, replacing the bracketed placeholders). Format floats to exactly 4 decimal places.

```text
REPORT FOR TX {TxID}
User: {User}
Card: {MaskedCard}
Norm_Amount: {NormAmount:.4f}
Rolling_Avg: {RollAvg:.4f}
---
```

**Execution:**
Once you have written the code, compile and run your Rust program to generate `/home/user/clean_report.txt`. Ensure all numbers are accurately calculated as 64-bit floats.