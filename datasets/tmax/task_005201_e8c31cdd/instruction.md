You are acting as a compliance officer auditing a financial system for money laundering risks. Your goal is to trace multi-hop fund transfers originating from a specific monitored account and determine how much capital is flowing into "HIGH" risk accounts through intermediary nodes.

You have been provided with two data exports in `/home/user/audit_data/`:
1. `accounts.csv` - Contains account mappings and risk tiers.
   Format: `account_id,risk_level`
2. `transfers.csv` - Contains direct transfer records.
   Format: `tx_id,source_id,target_id,amount`

Your task is to write a C program that builds a graph from this data, traverses it, and performs an analytical aggregation of the results. 

Write your C code in `/home/user/audit.c` and compile it to `/home/user/audit`. When executed, the program must generate a report at `/home/user/flagged_paths.csv` containing the processed results.

**Processing Requirements:**
1. **Graph Traversal:** Find all valid paths originating from account `A100` to any account marked as `HIGH` risk in `accounts.csv`.
2. **Path Constraints:** 
   - A path can have a maximum length of 3 hops (i.e., a maximum of 3 transfers / 4 accounts in the chain).
   - Paths must not contain cycles (do not visit the same account twice in a single path).
3. **Aggregation:** For each valid path, calculate the `total_amount` transferred (the sum of the `amount` of all transfers in that specific path).
4. **Window Function / Ranking:** For each distinct destination `HIGH` risk account, rank the incoming paths based on the `total_amount` in descending order. The path with the highest total amount gets rank 1. If amounts tie, rank them alphabetically by the path string.

**Output Format:**
Create a CSV file at `/home/user/flagged_paths.csv` with NO header row.
Format: `destination_id,path_string,total_amount,rank`
- `destination_id`: The ID of the HIGH risk account at the end of the path.
- `path_string`: The accounts in the path separated by `->` (e.g., `A100->A101->A102`).
- `total_amount`: Integer sum of transfer amounts.
- `rank`: Integer rank of the path for that specific destination.

Sort the final lines in `/home/user/flagged_paths.csv` by `destination_id` alphabetically (ascending), and then by `rank` (ascending).