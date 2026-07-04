You are acting as an AI assistant to a compliance officer auditing an internal financial system. We suspect that certain accounts are engaging in circular transactions to obfuscate fund origins (a pattern structurally similar to transaction deadlocks).

We have obtained a raw data dump in the form of an SQLite database located at `/home/user/finance_data.db`. However, the original developers used SQLite merely as a NoSQL document store, meaning the schema is completely undocumented and relies heavily on nested JSON. 

Your task is to:
1. Reverse engineer the schema of `/home/user/finance_data.db` to understand how the transaction documents are stored.
2. Install any necessary development libraries for C (e.g., SQLite3 development headers).
3. Write a C program named `/home/user/audit.c` that connects to this database and extracts the transaction graph.
4. Using graph traversal in C, identify all circular transaction chains of length EXACTLY 3 (e.g., Account A sends to Account B, Account B sends to Account C, and Account C sends back to Account A). A single transaction is directed.
5. Aggregate the total monetary amount involved across all transactions that participate in *any* 3-account cycle.
6. The C program must output its final findings to a file named `/home/user/audit_report.json` in the following exact format:
```json
{
  "total_3_cycles": <integer representing the number of unique 3-cycles>,
  "total_cycle_exposure": <integer representing the sum of amounts of all transactions in these 3-cycles>
}
```
*Note: A cycle A->B->C->A is the same as B->C->A->B. Count it as 1 unique cycle. Only count the transaction amounts once per transaction, even if they somehow participate in multiple cycles.*

Compile your C program to an executable named `/home/user/audit_runner` and execute it to produce the report. 
Do not assume any prior knowledge of the table names or JSON keys—you must inspect the database to figure out the NoSQL structure.