You are a database administrator tasked with investigating a series of transaction deadlocks in a Neo4j graph database.

A log of concurrent transactions has been exported from the database's NoSQL aggregation pipeline into a JSON file at `/home/user/tx_data.json`. Each transaction executes a series of Cypher queries. The application currently uses poor schema access patterns, acquiring exclusive write locks on `User` nodes sequentially during a transaction. 

A deadlock occurs if two concurrent transactions attempt to lock the same two `User` nodes but in the reverse order (e.g., Transaction A locks Node X then Node Y, while Transaction B locks Node Y then Node X).

Your task:
1. Initialize a new Rust project at `/home/user/tx_analyzer`.
2. Write a Rust program that parses `/home/user/tx_data.json`.
3. Analyze the Cypher queries within each transaction to extract the sequence of `uid` values locked. (Queries always take the form: `MATCH (n:User {uid: <NUMBER>}) SET ...`).
4. Identify the single pair of transactions that creates a potential deadlock (locking exactly the same two UIDs, but in reverse order).
5. Output the result to a log file at `/home/user/resolution.txt` containing the IDs of the two deadlocking transactions, sorted alphabetically, followed by the optimized (deadlock-free) parameterized queries for those transactions. To prevent deadlocks, the optimized transactions must always lock the node with the numerically *lower* UID first.

The output format in `/home/user/resolution.txt` must exactly match this template:
```
Deadlock: TX_A, TX_B
Safe_TX_A_Step1: MATCH (n:User {uid: $lower_uid}) SET n.status = 'updated'
Safe_TX_A_Step2: MATCH (n:User {uid: $higher_uid}) SET n.status = 'updated'
Safe_TX_B_Step1: MATCH (n:User {uid: $lower_uid}) SET n.status = 'updated'
Safe_TX_B_Step2: MATCH (n:User {uid: $higher_uid}) SET n.status = 'updated'
```
(Replace `TX_A`, `TX_B`, `$lower_uid`, and `$higher_uid` with the actual transaction IDs and the numeric UID values involved in the deadlock).

Constraints:
- You must use Rust to analyze the data.
- Do not install external databases; process the JSON file directly.
- Standard libraries and popular crates (like `serde`, `serde_json`, `regex`) are permitted.