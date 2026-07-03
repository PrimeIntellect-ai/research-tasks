You are assisting a compliance officer who is auditing a financial network for suspected circular trading patterns (which conceptually mirror transaction deadlocks in database systems). You have been provided with a dataset of financial transfers.

Your task is to write a Bash script `/home/user/run_audit.sh` that processes a CSV file located at `/home/user/transfers.csv` (which contains headers: `tx_id,sender,receiver,amount`) and performs graph-based query analysis using `sqlite3`. 

The script must analyze the transaction graph and output a strict JSON file to `/home/user/audit_results.json` containing the following insights:

1. **Cycle Detection (Pattern Matching):** Find all accounts involved in any circular transaction chain of exactly length 3 (i.e., A sends to B, B sends to C, C sends to A). Note: The same account can be part of multiple cycles.
2. **Account Centrality:** Among all the unique accounts identified in step 1, determine which one has the highest overall "degree centrality" in the *entire* network. Degree centrality here is defined as the total number of transactions an account is involved in (sum of transactions sent + transactions received). If there is a tie, pick the account ID that comes first alphabetically.
3. **High-Risk Filtering & Sorting:** Find the top 2 highest-value transactions (by `amount`) where *both* the sender and the receiver are accounts identified in the cycle detection step (they don't have to be in the same cycle, just in the pool of cycle-associated accounts).

Your Bash script should:
- Ensure `sqlite3` is installed or install it if necessary.
- Load the CSV into an in-memory SQLite database or a temporary file.
- Execute the necessary SQL queries (using CTEs, joins, or other graph query equivalents).
- Format the output exactly as the following JSON structure and save it to `/home/user/audit_results.json`:

```json
{
  "cycle_accounts": ["A1", "A2", "A3", "..."], 
  "highest_degree_cycle_account": "A1",
  "top_cycle_transactions": [99, 42]
}
```
*Note for JSON formatting:*
- `cycle_accounts` should be a sorted (alphabetical) array of strings representing the unique account IDs.
- `highest_degree_cycle_account` should be a string.
- `top_cycle_transactions` should be an array of integers representing the `tx_id`s of the top 2 transactions, sorted by amount in descending order.

Make sure your script is executable (`chmod +x /home/user/run_audit.sh`). Do not include any hardcoded assumptions about the CSV data; it will be evaluated against the provided file.