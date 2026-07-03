You are a data engineer building an ETL pipeline to merge unstructured customer service logs with a structured transaction database. 

You have two data sources:
1. CRM Logs: A directory of text files located at `/home/user/data/crm/`. Each file contains unstructured notes from a customer service representative.
2. Transactions: A directory of JSON files located at `/home/user/data/transactions/`. Each file contains an array of transaction records.

Your goal is to extract information, find matching records, mask sensitive data, and output a joined CSV file.

Create a Python script at `/home/user/etl.py` that performs the following steps:
1. **Parallel Extraction**: Use Python's `multiprocessing` module to read all text files in `/home/user/data/crm/` in parallel. From each file, extract the customer's name and email address using regular expressions. 
   - *Hint*: Names in the text files are always preceded by "Customer " and followed by " called" or " sent". E.g., "Customer John Doe called." -> Name is "John Doe".
   - *Hint*: Emails are standard format, e.g., "reach him at john@example.com."
2. **Data Masking**: 
   - Mask the extracted emails by keeping only the first letter, replacing the rest of the local part with `***`, and keeping the domain intact (e.g., `john@example.com` becomes `j***@example.com`).
   - Mask the `cc` (credit card) field in the transaction JSON files by replacing all but the last 4 digits with asterisks (e.g., `1111222233334444` becomes `************4444`).
3. **Similarity Join**: The names in the CRM logs might have slight typos compared to the Transaction database. Join a CRM record with a Transaction record if the Levenshtein distance between the CRM name and the Transaction name is **less than or equal to 2**. 
4. **Output**: Write the successfully joined records to `/home/user/output/joined_data.csv`. The CSV must have the following exact header and be sorted alphabetically by `tx_id`:
   `tx_id,crm_name,tx_name,masked_email,masked_cc`

Run your script to generate the final CSV.