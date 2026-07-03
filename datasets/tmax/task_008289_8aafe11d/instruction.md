You are acting as a compliance officer auditing an internal financial system for potential money laundering. You have been provided with an undocumented SQLite database located at `/home/user/compliance.db`. 

Your objective is to find suspicious circular fund flows (cycles) that consist entirely of "anomalous" transactions. 

Please perform the following steps:

1. **Data Model Reverse Engineering**: Inspect `/home/user/compliance.db` to understand the schema. There is a table recording transactions.
2. **Window Functions & Filtering**: Use SQL to extract all "anomalous" transactions. A transaction is considered anomalous if its `amount` is strictly greater than the average `amount` of the preceding 2 transactions originating from the *same* source account. 
   * Preceding transactions are determined by strict ordering of the `timestamp` column. 
   * If an account has fewer than 2 preceding transactions at the time of a given transaction, the average should be computed over the available preceding transactions. If there are 0 preceding transactions, the average is considered to be 0.
   * Save the anomalous transactions (in CSV format, without headers) to `/home/user/filtered_tx.csv` using the format: `tx_id,src_account,dst_account,amount,timestamp`.
3. **Knowledge Graph Pattern Matching**: Write a C program at `/home/user/graph_audit.c` that reads `/home/user/filtered_tx.csv`. The program must find all cyclic transaction patterns of length exactly 3 (i.e., Account A -> Account B -> Account C -> Account A) where:
   * All three edges in the cycle are present in the `filtered_tx.csv` file.
   * The maximum timestamp difference between any two transactions in the cycle is less than or equal to 86400 seconds (1 day).
4. **Output Generation**: Your C program must write the identified compliance violations to `/home/user/violations.txt`. Each line should represent one cycle, formatted as `A,B,C` where A, B, and C are the account IDs. 
   * To ensure consistency, represent the cycle starting with the account ID that initiated the chronologically earliest transaction in the cycle.
   * If there are multiple cycles, print each on a new line, sorted ascending by the starting account ID.

Compile your C program, run it, and ensure `/home/user/violations.txt` is populated correctly.