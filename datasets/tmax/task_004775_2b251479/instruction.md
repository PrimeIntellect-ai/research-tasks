You are a Database Administrator tasked with processing exported NoSQL transaction logs and resource dependency graphs to identify deadlocking concurrent transactions.

You have been provided with two data files in your home directory:
1. `/home/user/tx_locks.json`: A JSON NoSQL export containing a list of document objects representing transaction lock states. Each document has the following structure:
   `{"tx_id": "T01", "resource": "R10", "state": "GRANTED", "timestamp": 1620000001}`
   The `state` can be either `"GRANTED"` or `"WAITING"`.

2. `/home/user/resource_graph.nt`: An N-Triples format graph file representing resource dependencies. Each line represents a directed edge indicating that one resource logically depends on another resource:
   `<R10> <dependsOn> <R15> .`

**Your Goal:**
Write a Python script at `/home/user/find_deadlocks.py` that processes these files and outputs a report of deadlocked transaction pairs. 

A deadlock between two transactions, `TxA` and `TxB`, occurs when:
1. `TxA` is `WAITING` on some resource `Res1`.
2. `Res1` `<dependsOn>` `Res2` (according to the graph file).
3. `Res2` is `GRANTED` to `TxB`.
4. At the same time, `TxB` is `WAITING` on some resource `Res3`.
5. `Res3` `<dependsOn>` `Res4`.
6. `Res4` is `GRANTED` to `TxA`.

Your script must:
1. Parse both the JSON file and the N-Triples file.
2. Identify all pairs of deadlocked transactions based on the exact criteria above.
3. Consolidate the pairs such that the transaction ID that is lexicographically smaller is always the first transaction in the pair (`tx_1`, `tx_2` where `tx_1 < tx_2`).
4. Sort the resulting list of unique deadlocks by the minimum timestamp involved in the deadlock (the lowest timestamp among the four events: the two WAITING and two GRANTED events for that pair) in **ascending** order. If there's a tie, sort by `tx_1` ascending.
5. Limit (paginate) the results to output only the **top 5** oldest deadlocks.
6. Export the result to a CSV file at `/home/user/deadlocks_report.csv` with the exact header: `tx_1,tx_2,min_timestamp`.

Run your script to ensure the CSV is generated correctly. Do not install any external libraries (like `rdflib` or `pandas`); use Python's standard library.