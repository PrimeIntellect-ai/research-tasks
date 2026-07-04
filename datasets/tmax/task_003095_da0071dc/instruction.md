You are tasked with helping a data scientist clean and process a messy transaction log dataset to calculate merchant totals for a specific tax region. 

Here is what you need to do:

1. **Information Extraction**:
   There is a scanned receipt image located at `/app/receipt_sample.png`. Extract the text from this image to find the "Tax Region Code" (it appears as `TAX_REGION: <code-here>`). You'll need this code to filter the dataset.

2. **Data Processing (Rust)**:
   We have a messy dataset at `/app/transactions.jsonl`. Each line is a JSON object in a "wide" format, representing a batch of transactions for a specific `merchant_id`. It looks roughly like this:
   `{"merchant_id": "M123", "txn_1_amt": 15.50, "txn_1_desc": "Coffee shop [Region: R-99]", "txn_2_amt": 12.00, "txn_2_desc": "Muffins [Region: R-99]", ...}`
   
   However, the dataset has a known issue: the system that exported it occasionally corrupted the strings by improperly escaping unicode characters (e.g., printing `\\u0026` instead of `&`). 

   Write a Rust program that performs the following pipeline:
   - Reads the JSON-lines file.
   - Cleans the string descriptions by fixing the escaped unicode (you can simply unescape standard `\uXXXX` sequences that were double-escaped, or extract the needed parts safely).
   - Reshapes the data from wide to long format. Each transaction (amount and description) should be treated as an individual record.
   - Uses Regular Expressions to extract the "Region" code from the transaction descriptions.
   - Filters the records, keeping ONLY the transactions that belong to the tax region code you extracted from `/app/receipt_sample.png`.
   - Sorts and groups the filtered records by `merchant_id`, calculating the total sum of amounts for each merchant in that region.
   
3. **Output**:
   Your Rust program must output the final aggregated data as a CSV file to `/home/user/summary.csv`. The CSV should have headers: `merchant_id,total_amount`. The `total_amount` should be rounded to 2 decimal places.

To complete the task, set up a Cargo project in `/home/user/process_txns`, write your Rust code, run it, and generate the final CSV file. The verifier will evaluate your CSV by comparing its aggregated totals against the reference data using a numeric error threshold.