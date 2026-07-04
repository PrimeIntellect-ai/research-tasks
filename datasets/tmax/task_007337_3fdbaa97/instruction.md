You are an AI assistant helping a compliance officer audit a financial system.

We have exported recent transaction networks into an RDF graph file located at `/home/user/transactions.ttl`. 
We also have a local SQLite database `/home/user/audit.db` which tracks the audit status of flagged accounts. 
Our automated audit pipeline runs concurrent scripts to update the database, but we are currently experiencing a deadlock issue.

Your task consists of two parts:

Part 1: Graph Pattern Matching
Write a script (in the language of your choice, though Python with `rdflib` is recommended) to query `/home/user/transactions.ttl` using SPARQL. 
You need to identify all accounts that are part of a circular transfer loop of exactly length 3 (i.e., Account A transfers to Account B, B transfers to C, and C transfers back to A).
Write the URIs of all accounts involved in such 3-step cycles to `/home/user/flagged_accounts.txt`. 
The file must contain exactly one URI per line, sorted alphabetically.

Part 2: Deadlock Resolution
We have two audit scripts, `/home/user/worker1.py` and `/home/user/worker2.py`, which are executed concurrently. 
Because of how SQLite handles locks during concurrent read-then-write transactions, running them simultaneously results in a deadlock (`database is locked` error).
Modify `/home/user/worker2.py` so that it avoids the deadlock when run concurrently with `worker1.py`. You must keep the same logical operations (a `SELECT` followed by an `UPDATE`), but you should modify how the database transaction is initiated to prevent the locking conflict.

Constraints:
- Do not modify `/home/user/worker1.py`.
- You may install any necessary packages (like `rdflib`).