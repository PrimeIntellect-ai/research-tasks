You are acting as a technical compliance officer auditing a legacy financial application. 

We have discovered an undocumented SQLite database at `/home/user/legacy_system.db`. We suspect this database contains transaction records that include prohibited "circular transfers" (where funds move in a closed loop, e.g., Account A -> Account B -> Account C -> Account A) intended to obscure funds or cause transactional deadlocks.

Your task is to reverse engineer the data model, build a data extraction pipeline, and generate a validated compliance report. 

Specifically, you need to:
1. Inspect the database `/home/user/legacy_system.db` to understand its schema. The table containing transfers is not documented.
2. Write a Python script `/home/user/audit_pipeline.py` that connects to this database and identifies all length-3 circular transfers (A -> B -> C -> A).
3. A cycle is only considered a compliance violation if all three transfers occur within a 60-second window (inclusive) of each other (i.e., the difference between the maximum and minimum timestamp in the cycle is <= 60 seconds).
4. Calculate the `total_volume` of each cycle (the sum of the transfer amounts in the cycle).
5. The script must output a strictly validated JSON file at `/home/user/compliance_report.json`.

The output JSON must be a list of objects adhering to this exact schema:
```json
[
  {
    "cycle_id": "<integer, defined as the minimum transaction ID involved in the cycle>",
    "accounts": ["<string, account ID>", "<string>", "<string>"],
    "total_volume": "<float, sum of the three transaction amounts>"
  }
]
```
Note: The `accounts` array in the JSON output must be sorted alphabetically to ensure deterministic reporting.

Run your script to produce the final `/home/user/compliance_report.json` file.