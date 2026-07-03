You are a compliance officer auditing a corporate financial system for illicit money flows. 
A snapshot of recent financial activity has been provided to you as a SQLite database located at `/home/user/financial_audit.db`.

The database has the following schema:
- `accounts` table:
  - `account_id` (TEXT): Unique identifier for the account.
  - `account_type` (TEXT): Type of account (e.g., 'domestic', 'offshore').
  - `risk_score` (INTEGER): A compliance risk score from 0 to 100. Accounts with a score > 80 are considered "high-risk".
- `transactions` table:
  - `tx_id` (TEXT): Unique identifier for the transaction.
  - `source_account` (TEXT): The `account_id` initiating the transfer.
  - `target_account` (TEXT): The `account_id` receiving the transfer.
  - `amount` (REAL): The transaction amount.

Your task is to analyze this data to identify key hubs and potential money laundering paths. You may use any programming language or tools you prefer (e.g., Python with sqlite3 and networkx).

Perform the following steps:
1. Construct a directed graph from the `transactions` table, where nodes are `account_id`s and directed edges represent transactions from `source_account` to `target_account`.
2. Compute the PageRank of all accounts in the network using the standard algorithm (if using Python, use `networkx.pagerank` with default parameters: alpha=0.85). Sort the accounts by their PageRank in descending order to find the top 3 most central accounts. If there is a tie, sort alphabetically by `account_id`.
3. Find the shortest path (minimum number of transaction hops) from *any* "high-risk" account (risk_score > 80) to *any* "offshore" account (`account_type` = 'offshore'). If there are multiple paths with the exact same minimum length, choose the one whose starting `account_id` is alphabetically first.

Once you have completed your analysis, save your findings in a JSON file at `/home/user/audit_report.json` with the exact following structure:
```json
{
  "top_3_pagerank_accounts": ["account_id_1", "account_id_2", "account_id_3"],
  "shortest_illicit_path": ["start_high_risk_account", "intermediary_account_if_any", "end_offshore_account"]
}
```