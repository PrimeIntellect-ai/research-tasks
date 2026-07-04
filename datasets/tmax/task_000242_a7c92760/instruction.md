You are a compliance officer auditing a financial system to detect potential money laundering rings. The system's transaction logs need to be analyzed to find circular cash flows and identify the most critical accounts acting as hubs in these schemes.

Your task is to analyze transaction data stored in a local MongoDB database using a combination of NoSQL aggregation pipelines and Python graph analytics.

**Environment Setup**
1. A setup script is provided at `/home/user/setup_db.sh`. Execute this script to download, start a local MongoDB instance (on default port 27017), and populate the `audit` database with a `financial_tx` collection.
2. The collection contains transaction documents with the following schema:
   `{"sender": "string", "receiver": "string", "amount": number, "currency": "USD", "timestamp": "string"}`

**Analysis Requirements**
Create a Python script at `/home/user/audit.py` that performs the following:
1. Connects to the local MongoDB `audit` database.
2. Executes a **MongoDB aggregation pipeline** to calculate the total transaction amount between each `sender` and `receiver` pair. Filter the results to keep ONLY pairs where the total aggregated amount transferred from the sender to the receiver is strictly greater than `10000`.
3. Using the filtered pairs as directed edges (from `sender` to `receiver`, ignoring edge weights), construct a directed graph using the `networkx` library.
4. Identify all accounts (nodes) that are part of at least one directed cycle.
5. Compute the PageRank for all nodes in the entire directed graph using `networkx.pagerank` with `alpha=0.85`.
6. Identify the accounts that are **both** part of a cycle AND have the highest PageRank.

**Output Specification**
Your script must write the top 3 accounts meeting the above criteria (in a cycle, highest PageRank) to a JSON file at `/home/user/flagged_accounts.json`.
The output must be a JSON array of objects, sorted in descending order by PageRank. Format exactly like this:
```json
[
  {"account": "AccX", "pagerank": 0.1523},
  {"account": "AccY", "pagerank": 0.1201},
  {"account": "AccZ", "pagerank": 0.0984}
]
```
Ensure your script installs any necessary Python dependencies (like `pymongo` and `networkx`) or install them manually before running your script.