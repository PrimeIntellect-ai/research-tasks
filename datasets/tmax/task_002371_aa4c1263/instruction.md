You are a compliance officer auditing a financial system for anomalous transaction patterns. The engineering team recently discovered that the system can suffer from a "deadlock" state when two users initiate simultaneous transactions to each other at the exact same millisecond. 

You have been provided an export of the transaction database as a JSON Lines file (simulating a NoSQL document store) located at `/home/user/transactions.jsonl`. 

The schema for each JSON object in the file is:
`{"tx_id": "string", "sender": "string", "receiver": "string", "amount": float, "timestamp": "YYYY-MM-DDThh:mm:ssZ"}`

Your task is to write a Bash script at `/home/user/find_deadlocks.sh` that takes a date parameter (in `YYYY-MM-DD` format) and identifies all deadlock transaction pairs occurring on that specific date.

A "deadlock pair" is defined as two separate transactions where:
1. Transaction A's `sender` matches Transaction B's `receiver`.
2. Transaction A's `receiver` matches Transaction B's `sender`.
3. Both transactions have the exact same `timestamp`.
4. Both transactions occurred on the date provided to the script.

Requirements:
1. Write a parameterized Bash script `/home/user/find_deadlocks.sh` that accepts a single date string argument (e.g., `2023-10-01`).
2. The script must process `/home/user/transactions.jsonl` using command-line tools (like `jq`, `awk`, or a small embedded inline Python/Ruby script inside the bash script).
3. The script must write the results to `/home/user/deadlocks.log`.
4. Each line in `deadlocks.log` should represent one deadlock pair in the format: `TXID_1,TXID_2`.
5. For each pair, the transaction IDs must be sorted alphabetically (e.g., `T001,T002` instead of `T002,T001`).
6. The lines in `deadlocks.log` must be sorted alphabetically.
7. Ensure the script is executable (`chmod +x`). 

Execute your script with the argument `2023-10-01` to generate the final `/home/user/deadlocks.log` file for the automated verification suite.