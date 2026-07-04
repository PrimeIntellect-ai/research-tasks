You are acting as a compliance officer auditing a financial system for suspicious activities. You have been provided with an SQLite database at `/home/user/financial_audit.db` containing a single table `wire_transfers` with the following schema:
`tx_id INTEGER PRIMARY KEY, sender TEXT, receiver TEXT, amount REAL, timestamp DATETIME`

Your task is to detect circular money flow patterns that may indicate money laundering. Specifically, you need to find all directed cycles of exactly 3 distinct accounts (e.g., A -> B -> C -> A) that meet the following criteria:
1. The transfers must occur in strict chronological order (A -> B happens before B -> C, which happens before C -> A).
2. The three accounts involved must be distinct.
3. To avoid duplicate cycles in the output (e.g., reporting A->B->C->A and B->C->A->B as separate cycles), ensure that the first account in your output (`acct_A`) is alphabetically the smallest of the three accounts.

For each discovered cycle:
- Calculate the `cycle_total`, which is the sum of the amounts of the 3 transfers making up the cycle.
- Assign a `risk_rank` to each cycle using an analytical window function, ranking them in descending order based on `cycle_total`. (Rank 1 goes to the highest total).

Write and execute a query to extract this information and export the results to a CSV file at `/home/user/circular_flows.csv`.
The CSV must include headers and contain exactly these columns in this order: `acct_A`, `acct_B`, `acct_C`, `cycle_total`, `risk_rank`.

Use standard command-line tools (like `sqlite3`) to accomplish this task.