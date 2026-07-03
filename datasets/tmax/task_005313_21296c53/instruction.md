You are a data analyst investigating a series of suspected money laundering rings using a multi-service data pipeline. 

Your environment has a startup script located at `/app/start_services.sh`. When executed, this script brings up a local MongoDB database on port 27017 and a mock banking API on port 5000. 

Your goal is to build a detector that analyzes transaction graphs to separate legitimate trading behavior from illicit money laundering cycles. 

You have been provided with two directories containing transaction data in CSV format:
1. `/home/user/corpora/clean/` - Contains CSV files of normal, legitimate transaction networks.
2. `/home/user/corpora/evil/` - Contains CSV files of transaction networks that feature money laundering. 

A money laundering network ("EVIL") is defined strictly by the presence of a directed financial cycle (e.g., Account A -> Account B -> Account C -> Account A) involving at least 3 distinct accounts, where the bottleneck (minimum) transaction amount in the cycle is greater than or equal to $50,000. 

Your tasks are:
1. Run `/app/start_services.sh` to ensure the background services are active.
2. Create a script at `/home/user/detector.py` (or `.js`, `.sh`, etc.) that takes a single command-line argument: the absolute path to a transaction CSV file.
3. The script must ingest the CSV into MongoDB, use NoSQL aggregation pipelines (such as `$graphLookup`) or in-memory graph projection (like NetworkX) to reverse engineer the transaction schema and find cycles.
4. The script must output exactly `EVIL` to standard output if the network contains a money laundering cycle matching the criteria above, or `CLEAN` if it does not.

You must ensure that your detector correctly classifies 100% of the CSV files in both the `clean` and `evil` directories.

The CSV files have the following headers: `source_account,target_account,timestamp,amount`.

Build your detector, test it against the corpora, and ensure your final script is located at `/home/user/detector.py`.