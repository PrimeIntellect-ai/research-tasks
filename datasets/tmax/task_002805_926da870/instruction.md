You are a data analyst who needs to process a local dataset of e-commerce transactions using Python and SQLite. 

There is a CSV file at `/home/user/transactions.csv` containing raw transaction records with the following headers:
`tx_id,date,category,amount,customer_id`

Your task is to write a Python command-line utility at `/home/user/query_tool.py` that loads this CSV into an in-memory SQLite database and executes parameterized queries based on user arguments. 

The script `query_tool.py` must use the standard library `argparse`, `csv`, and `sqlite3` modules, and it must support the following arguments:
- `--category`: (String) Filter transactions by an exact category match.
- `--min-amount`: (Float) Filter transactions where the amount is greater than or equal to this value.
- `--sort`: (String) Sort the results. The format will be `column_name:direction` (e.g., `amount:desc` or `date:asc`).
- `--limit`: (Integer) Limit the number of returned records.
- `--offset`: (Integer) Number of records to skip before returning.

The script must print ONLY the `tx_id` of the resulting records to standard output, one per line.
Important: To prevent injection, you MUST use parameterized SQLite queries (`?` placeholders) for the `--category`, `--min-amount`, `--limit`, and `--offset` values. (Column names and sort directions for the `ORDER BY` clause can be formatted into the query safely since they cannot be parameterized in standard SQL).

After completing the script, you must execute it to generate two report files.

**Report 1:**
Run your tool to find `Electronics` transactions with an amount of at least `100`, sorted by `amount:desc`, returning a maximum of `2` records with no offset.
Pipe the standard output of this run to `/home/user/q1_output.txt`.

**Report 2:**
Run your tool to find `Books` transactions, sorted by `date:desc`, returning `3` records after skipping the first `1` (offset 1). No minimum amount.
Pipe the standard output of this run to `/home/user/q2_output.txt`.