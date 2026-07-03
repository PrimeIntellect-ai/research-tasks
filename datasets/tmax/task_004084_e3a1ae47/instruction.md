You are a data analyst tasked with processing transaction data to identify key nodes in a financial network. 

You have been provided with two CSV files in your home directory:
1. `/home/user/accounts.csv` - Contains account metadata. Columns: `account_id` (int), `status` (string: ACTIVE or INACTIVE), `type` (string).
2. `/home/user/transactions.csv` - Contains transaction records. Columns: `source` (int), `target` (int), `amount` (float).

Your objective is to write a C++ program at `/home/user/analyze.cpp` that performs the following steps:
1. Load the CSV data into an embedded SQLite in-memory database (using the `sqlite3` C API).
2. Construct and execute a SQL query to filter the transactions. You must only keep transactions where the `amount` is strictly greater than 500.0 AND both the `source` and `target` accounts have a `status` of 'ACTIVE'.
3. Using the results of this complex join, build an in-memory directed graph in C++.
4. Calculate the out-degree centrality for every account that appears in the filtered transaction set (either as a source or a target). The out-degree is the number of outgoing filtered transactions from that account.
5. Write the top 3 accounts with the highest out-degree centrality to `/home/user/top_accounts.csv`. The output must be exactly 3 lines, formatted as `account_id,out_degree`. If there is a tie in out-degree, sort by `account_id` in ascending order.

Requirements:
- Ensure you install any necessary SQLite development libraries (e.g., `libsqlite3-dev` on Debian/Ubuntu) before compiling.
- Compile your C++ code to an executable named `/home/user/analyze`. Use the `-lsqlite3` flag.
- Execute your program so that `/home/user/top_accounts.csv` is generated.
- The output file must not contain a header row.