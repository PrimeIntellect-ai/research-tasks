You are acting as a technical compliance officer auditing an internal trading system. We suspect that certain accounts are exploiting race conditions, which manifest as transaction deadlocks in the system logs, to artificially inflate their balances. 

I have provided a SQLite database file at `/home/user/finance.db`. I do not have the exact database schema, so you will need to inspect the database yourself to understand the tables, columns, and relationships (specifically looking for transaction records and system event logs).

Your task is to write a C++ program that processes this data to identify suspicious accounts and calculate their net completed transaction volumes. 

Here are the specific audit rules:
1. **Identify Suspicious Accounts**: Find all accounts that have experienced two or more `ERR_DEADLOCK` events within *any* rolling 3600-second (1 hour) window in the event logs. You must evaluate this using SQL window functions or self-joins.
2. **Calculate Net Volume**: For *only* these suspicious accounts, calculate their net completed transaction volume from the transaction records. 
   - Net volume is defined as the sum of all 'CREDIT' amounts minus the sum of all 'DEBIT' amounts for transactions with a 'COMPLETED' status. 
   - Ignore transactions that are 'ROLLED_BACK' or 'FAILED'.
3. **Generate Report**: Your C++ program must execute these queries and write the final output to `/home/user/audit_results.json`. 

The output must be a valid JSON array of objects, sorted by `account_id` in ascending order, strictly matching this schema:
```json
[
  {
    "account_id": 105,
    "net_volume": 1250.50
  },
  ...
]
```
Ensure that `net_volume` is formatted to exactly two decimal places.

**Constraints & Environment:**
- Write your solution in a single C++ file at `/home/user/audit.cpp`.
- Compile it to an executable named `/home/user/audit`.
- You must use the SQLite C/C++ API (`<sqlite3.h>`). The `libsqlite3-dev` package is already installed on the system.
- You can generate the JSON string manually in C++ or download a header-only library like `nlohmann/json` if you prefer.
- Run your executable to produce the `/home/user/audit_results.json` file.