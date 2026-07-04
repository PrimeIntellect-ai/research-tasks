You are a compliance officer conducting an audit of a company's internal financial systems. You have been provided with an SQLite database at `/home/user/financial_audit.db` and a proprietary, compiled risk-scoring tool at `/app/risk_scorer`.

Your objective is to generate a comprehensive compliance report by extracting transaction lineages, calculating running totals, and scoring them using the proprietary tool. 

However, there is a known issue: the system administrators suspect that the database index on the `transactions` table has been corrupted and is returning stale or missing rows during lookups. You must work around or fix this corruption to retrieve the correct data.

Here are the requirements for your audit:
1. **Bypass or Fix Corruption:** Inspect the schema of `/home/user/financial_audit.db`. Identify and bypass or drop the corrupted index on the `transactions` table so your queries return accurate results.
2. **Transaction Lineage (Recursive Query):** Write a query to reconstruct the transaction chains. Transactions are hierarchical (they have a `parent_tx_id`). For every transaction, determine its absolute root transaction ID.
3. **Department Aggregation (Window Functions):** Calculate the running total of transaction amounts per `department_id`, ordered by the transaction `timestamp`.
4. **Risk Scoring:** The binary `/app/risk_scorer` takes a single integer (a running total amount) as a command-line argument and prints a floating-point risk score to standard output.
5. **Final Output:** Write a Python script at `/home/user/generate_report.py` that performs these queries, queries the `/app/risk_scorer` binary for each row's running total, and outputs a CSV file at `/home/user/compliance_report.csv`.

The output CSV must have exactly this header and format:
`tx_id,root_tx_id,department_id,running_total,risk_score`
Order the CSV rows by `department_id` ascending, then `timestamp` ascending.

Ensure your Python script runs to completion and produces the correct CSV.