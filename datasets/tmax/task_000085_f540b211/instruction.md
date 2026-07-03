As a compliance officer auditing our financial systems, I need your help to trace a complex money flow pattern that looks like a cyclic transaction deadlock used for funds layering.

You have been provided with two datasets in the home directory:
1. `/home/user/accounts.csv` - Contains `account_id` and `risk_level`.
2. `/home/user/transactions.csv` - Contains `tx_id`, `source`, `target`, and `amount` (numeric).

Your task is to write a Python script at `/home/user/audit_graph.py` that analyzes this data as a directed graph to find a specific suspicious pattern.

The pattern you must find is a cycle of exactly 4 transactions involving 4 distinct accounts (e.g., A -> B -> C -> D -> A) that meets the following compliance criteria:
1. Every account in the cycle must have a `risk_level` of either `high_risk` or `offshore`.
2. The total sum of the `amount` of the 4 transactions forming this cycle must be strictly greater than 10,000.

There is exactly one such cycle in the dataset.
Once you identify the 4 accounts involved in this cycle, sort their `account_id`s in alphabetical order and export them as a JSON array to `/home/user/suspicious_cycle.json`.

For example, the output file should look exactly like this:
```json
["ACC1", "ACC2", "ACC3", "ACC4"]
```

Ensure your script runs successfully and produces the required JSON file.