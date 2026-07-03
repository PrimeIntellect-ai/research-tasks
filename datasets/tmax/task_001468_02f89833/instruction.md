You are a data analyst investigating a series of financial transactions. Some transactions may be causing system deadlocks, and others might have invalid account references due to a data export glitch. You have two files: `/home/user/accounts.csv` and `/home/user/transactions.csv`.

Your tasks:
1. **Schema Validation**: Identify all transactions in `transactions.csv` where either the `from_account` or `to_account` does NOT exist in the `account_id` column of `accounts.csv`. 
   - Write the `tx_id` of these invalid transactions to `/home/user/invalid_tx.txt`, one per line, sorted alphabetically.

2. **Deadlock Detection (Graph Projection)**: A "deadlock" happens when two accounts send money to each other (A -> B and B -> A) within the exact same minute.
   - Ignore the seconds in the timestamp (e.g., `2023-10-01 10:05:12` and `2023-10-01 10:05:45` both occurred in the minute `2023-10-01 10:05`).
   - Find all pairs of accounts that have a deadlock.
   - Output the results as a JSON array to `/home/user/deadlocks.json`.
   - The JSON must follow this exact schema, where `account1` is lexicographically strictly less than `account2`:
     ```json
     [
       {
         "account1": "<smaller_account_id>",
         "account2": "<larger_account_id>",
         "minute": "YYYY-MM-DD HH:MM"
       }
     ]
     ```

Use only Bash built-ins, coreutils, and standard CLI tools (like `awk`, `grep`, `sort`, `jq`). Do not use Python, Perl, or a database engine.