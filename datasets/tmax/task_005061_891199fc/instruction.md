You are a Database Reliability Engineer investigating a severe backup system failure caused by deadlocks between concurrent backup transactions.

Your task is to build a Python diagnostic tool that uses a local MongoDB instance to analyze transaction lock graphs and export deadlock cycles.

Phase 1: Environment Setup
1. Download MongoDB for Ubuntu 22.04: `wget https://fastdl.mongodb.org/linux/mongodb-linux-x86_64-ubuntu2204-7.0.5.tgz`
2. Extract it and start a local `mongod` instance running on port `27017` with the dbpath `/home/user/mongodb_data` (create this directory).
3. Install `pymongo` via pip.
4. There is a file at `/home/user/transactions.json` containing NoSQL documents representing backup transaction states. Load this data into a MongoDB database named `backup_db`, collection `transactions`.

Phase 2: Diagnostic Script
Write a Python script at `/home/user/analyze_deadlocks.py` that does the following:
1. Connects to your local MongoDB instance.
2. Uses the `argparse` module to accept a parameterized starting transaction ID via `--txid`.
3. Constructs a **NoSQL aggregation pipeline** using `$graphLookup` (a recursive/hierarchical query) to traverse the `waits_for` field of the documents, starting from the given `--txid`.
4. The pipeline must filter the results to detect if the starting transaction ID appears in its own `$graphLookup` hierarchy (indicating a deadlock cycle).
5. Extract the sequential chain of transaction IDs involved in the deadlock (from the starting transaction, through the transactions it waits for, until it loops back).
6. Perform format conversion and export this sequence to a CSV file at `/home/user/deadlock_report.csv`. 

The CSV must have the following headers exactly:
`sequence_order,tx_id,waits_for,operation`
Where `sequence_order` starts at 1 for the `--txid` provided, and increments for each transaction in the blocking chain.

Run your script for `--txid TX-42`.
`python3 /home/user/analyze_deadlocks.py --txid TX-42`

Ensure the final CSV file `/home/user/deadlock_report.csv` is correctly formatted.