You are assisting a compliance officer in auditing our financial systems. Recently, an automated report flagged millions of "suspicious" transactions, but we discovered this was due to a botched SQL query that used an implicit cross join, inflating the results. 

Your task is to correct the data retrieval process, map the relational data to our document store, find a specific money-laundering pattern (Knowledge Graph pattern matching), and output the results conforming to a strict schema. Finally, you must design an indexing strategy to optimize the queries.

There is a SQLite database located at `/home/user/financial.db` with the following schema:
- `accounts` (id INTEGER PRIMARY KEY, name TEXT, address_id INTEGER)
- `transactions` (tx_id INTEGER PRIMARY KEY, sender_id INTEGER, receiver_id INTEGER, amount REAL, timestamp DATETIME)
- `addresses` (id INTEGER PRIMARY KEY, address_text TEXT)

There is also a document store containing KYC (Know Your Customer) details for each account, located at `/home/user/entities.json`. It is a list of JSON objects: `{"account_id": 1, "high_risk": true, "business_type": "shell"}`.

Here is what you need to do:

1. **Fix the Data Retrieval**:
   The old, buggy query was:
   `SELECT t.tx_id, a1.name as sender, a2.name as receiver FROM transactions t, accounts a1, accounts a2 WHERE t.amount > 10000;`
   Write a Python script that connects to `/home/user/financial.db` and performs a correct join to find all transactions where the amount is strictly greater than 10000. Correctly link the sender and receiver.

2. **Knowledge Graph Pattern Matching**:
   Using both the database and `entities.json`, find all instances of the "High-Risk Circular Flow" pattern:
   - Account A sends a transaction > 10000 to Account B.
   - Account B subsequently (timestamp is strictly greater) sends any amount to Account C.
   - Account A and Account C share the exact same `address_id`.
   - At least one of the accounts (A, B, or C) is flagged as `"high_risk": true` in `entities.json`.
   Note: A, B, and C must be distinct accounts.

3. **Output Schema Validation**:
   Save the matched patterns to `/home/user/audit_results.json`. The file must strictly be a JSON array of objects, each with the following exact keys:
   - `initial_tx_id` (integer): the tx_id from A to B
   - `subsequent_tx_id` (integer): the tx_id from B to C
   - `sender_a_id` (integer)
   - `intermediary_b_id` (integer)
   - `receiver_c_id` (integer)
   - `shared_address_id` (integer)
   Order the JSON array by `initial_tx_id` ascending.

4. **Index Strategy Design**:
   Create a file `/home/user/indexes.sql` containing the optimal `CREATE INDEX` statements to speed up the queries required to find this pattern (filtering by amount, joining on sender/receiver, looking up addresses). Do not create indexes on primary keys (as SQLite does this automatically).

You may use any standard Python libraries. Do not use external services. Ensure your final JSON output strictly matches the requested schema.