You are a data analyst working entirely in the Linux terminal. You need to write a parameterized data querying script in Bash to process a large CSV file containing sales records.

A CSV file is located at `/home/user/sales.csv` with the following header:
`TransactionID,Date,Region,Category,Amount,SalesRep`

Create a Bash script at `/home/user/query_sales.sh` that acts as a simple querying engine. It must accept exactly 5 positional arguments in this order:
1. `REGION`: String. Filter records matching this exact region (column 3).
2. `MIN_AMOUNT`: Integer. Filter records where the Amount (column 5) is greater than or equal to this value.
3. `SORT_COL`: Integer (1-6). The 1-based column index to sort the filtered results by. Sorting must be descending. If sorting by Amount (column 5) or TransactionID (column 1), the sort must be numeric. Otherwise, it must be alphabetical.
4. `PAGE_NUM`: Integer. The 1-based page number for pagination.
5. `PAGE_SIZE`: Integer. The number of records per page.

The script must output the resulting rows (without the CSV header) to standard output. 

Requirements:
- Only use standard Bash built-ins and POSIX utilities (e.g., `awk`, `sort`, `head`, `tail`, `sed`). Do not use Python, Perl, or SQLite.
- Ensure the script is executable.
- The CSV columns are separated by commas. You can assume there are no quoted commas within the fields.

Example invocation:
`/home/user/query_sales.sh "West" 150 5 2 10`
This should filter for "West" region, Amount >= 150, sort descending numerically by Amount (column 5), and return the 2nd page of 10 results (i.e., results 11-20).