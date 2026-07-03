You are acting as an automated compliance auditing agent. A recent regulatory request requires us to identify "circular transaction patterns" in our financial network to detect potential money laundering. 

You have been provided an SQLite database at `/home/user/audit.db` containing two tables:
1. `accounts` 
   - `account_id` (INTEGER PRIMARY KEY)
   - `owner_name` (TEXT)
   - `region` (TEXT)
2. `transactions`
   - `tx_id` (INTEGER PRIMARY KEY)
   - `sender_id` (INTEGER)
   - `receiver_id` (INTEGER)
   - `amount` (REAL)
   - `tx_timestamp` (DATETIME)

Your task is to:
1. Identify 3-hop circular transaction chains. A 3-hop circle is defined as an exact sequence of transfers where Account A sends money to Account B, B sends to C, and C sends back to A. 
   - The time sequence must strictly follow: A->B timestamp < B->C timestamp < C->A timestamp.
2. Formulate an indexing strategy. Write SQL statements to create necessary indexes on the `transactions` table to optimize the joins required for this graph traversal.
3. Aggregate the results. For every account 'A' that initiated one or more of these 3-hop circles, calculate the total `amount` they sent in the initial A->B step across all their circular chains.
4. Write a Bash script at `/home/user/run_audit.sh` that executes your SQL commands (including index creation and the query) against `/home/user/audit.db`.
5. The script must output the final aggregated results to `/home/user/suspicious_accounts.csv` with the exact format: `account_id,owner_name,total_suspicious_sent` (without a header row), sorted by `account_id` in descending order.

Ensure your Bash script is executable (`chmod +x`) and runs without errors.