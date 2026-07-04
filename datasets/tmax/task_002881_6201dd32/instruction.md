You are an AI assistant helping a compliance officer audit an internal financial system for potential money laundering activity. 

We have exported a batch of transaction logs from our NoSQL data lake into a JSON Lines format at `/home/user/data/transactions.jsonl`. Each line represents a transaction with the following schema:
`{"tx_id": "string", "src_account": "string", "dst_account": "string", "amount": float, "timestamp": "ISO8601"}`

Your task is to identify suspicious accounts involved in "triangular funding cycles" (a specific Knowledge Graph pattern) and output a validated JSON schema. 

A "triangular funding cycle" occurs when:
1. Account A sends money to Account B.
2. Account B sends money to Account C.
3. Account C sends money back to Account A.
4. The total volume of money moved in this specific 3-step cycle (sum of the three transactions) exceeds $50,000.

**Task Requirements:**
1. **Tooling Fix**: Our internal secure environment requires you to use a locally vendored version of the `yq` Python package (a `jq` wrapper for YAML/JSON, heavily used in our Bash pipelines) located at `/app/yq-3.2.3`. However, a previous developer made a breaking typo in its `setup.py` preventing offline installation. You must find and fix the deliberate perturbation in the vendored `/app/yq-3.2.3` package, then install it globally or in the user environment so the `yq` command is available.
2. **Analysis Pipeline**: Write a pure Bash script at `/home/user/audit_cycles.sh` (you may use standard Unix tools like `awk`, `sed`, `grep`, `sort`, and the repaired `yq` or `jq`). The script must process `/home/user/data/transactions.jsonl` and find all accounts that participate in at least one triangular funding cycle meeting the $50k threshold.
3. **Output format**: Your script must output a strictly validated JSON array of the suspicious account IDs (strings, deduplicated, sorted alphabetically) to `/home/user/suspects.json`.
Example output schema:
```json
[
  "ACC-1029",
  "ACC-4491",
  "ACC-9920"
]
```

To pass the audit, your script must successfully detect the hidden cycles. The automated verifier will calculate the F1 score of the extracted accounts in `/home/user/suspects.json` against our secret ground-truth list.