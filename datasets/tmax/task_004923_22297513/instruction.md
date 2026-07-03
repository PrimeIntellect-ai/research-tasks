You are an analyst investigating financial transactions. You have been given a CSV file located at `/home/user/transactions.csv` containing chronological transaction data with the following headers:
`tx_id,sender_id,receiver_id,amount,timestamp`

Your task is to identify "anomalous" transactions using analytical aggregation and map them into a graph database format. 

An anomaly is defined strictly as:
A transaction whose `amount` is strictly greater than `2.0` times the average `amount` of *all preceding transactions* sent by that exact same `sender_id`.
Note: If a sender has no preceding transactions, their transaction cannot be evaluated as an anomaly (it is considered normal).

Please write a Bash script (you may use inline Python, SQLite, `awk`, etc.) that processes this CSV and generates a Cypher script to be loaded into a Neo4j database. 

The output file must be written to `/home/user/anomalies.cypher`.

For every anomalous transaction found, append the following Cypher statements (in this exact order, separated by newlines) into `/home/user/anomalies.cypher`:
```cypher
MERGE (s:User {id: "<sender_id>"})
MERGE (r:User {id: "<receiver_id>"})
CREATE (s)-[:SENT_ANOMALY {tx_id: "<tx_id>", amount: <amount>}]->(r);
```
Ensure each block of 3 statements ends with a semicolon after the `CREATE` statement, and that there is exactly one empty line between each anomaly block.

The output Cypher file must be deterministic and ordered chronologically by the timestamp of the anomalous transactions.