You are a Database Reliability Engineer (DBRE) analyzing a database lock snapshot to resolve concurrency issues. As part of managing backups, you took a snapshot of the current transaction lock graph, which is represented in an RDF format (Turtle). 

The lock snapshot is located at `/home/user/transactions.ttl`.

It uses the prefix `ex: <http://example.org/>` and contains triples describing transactions and resources using the predicates `ex:waitsFor` and `ex:heldBy`. A deadlock occurs when there is a cycle of two transactions: Transaction A waits for a resource held by Transaction B, while Transaction B waits for a resource held by Transaction A.

Your task is to write a Bash script at `/home/user/detect_deadlocks.sh` that does the following:
1. Downloads and extracts Apache Jena (use version 4.9.0 from `https://archive.apache.org/dist/jena/binaries/apache-jena-4.9.0.tar.gz`) into `/home/user/jena`.
2. Uses Jena's command-line tools (specifically `sparql`) to query the `/home/user/transactions.ttl` file.
3. The SPARQL query must identify all deadlocked pairs of transactions (cycles of length 2 as described above).
4. To avoid duplicate reports for the same deadlock, ensure the transaction ID for the first transaction is alphabetically less than the second transaction (e.g., if T1 and T2 are deadlocked, return T1 as the first and T2 as the second).
5. Extract only the local names of the transactions (e.g., "T1", not "http://example.org/T1").
6. The Bash script must parse the SPARQL output and generate a strictly formatted JSON array in `/home/user/deadlocks.json`.

The final JSON output must look exactly like this (sorted alphabetically by tx1):
```json
[
  {
    "tx1": "T1",
    "tx2": "T2"
  }
]
```

Ensure your script is executable (`chmod +x /home/user/detect_deadlocks.sh`) and runs to completion without manual intervention, producing the JSON file. Use basic Linux tools (`jq`, `grep`, `awk`, etc.) in combination with Jena to format the output.