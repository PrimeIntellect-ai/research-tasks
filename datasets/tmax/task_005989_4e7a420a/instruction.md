You are assisting a compliance officer who is auditing our internal transaction systems for potential race conditions and unauthorized overlapping resource mutations. 

We have exported the raw NoSQL audit logs to a JSON Lines file located at `/home/user/audit_logs.jsonl`. Because it comes from a loosely-structured NoSQL database, the schema is not strictly enforced.

Your task is to:
1. Reverse engineer the data model from the JSONL file. You will notice that events contain timestamps, transaction identifiers (sometimes called `req` or `tx`), event types, and nested payloads containing the targeted resource IDs.
2. Write a Python script `/home/user/audit.py` that parses this file, normalizes the data, and loads it into a local SQLite database at `/home/user/audit.db`.
3. Using SQL, write a query utilizing **Window Functions** to identify potential concurrency violations. A violation occurs when a specific resource receives a `write` event from a transaction, and then receives another `write` event from a *different* transaction within 500 milliseconds (i.e., time difference strictly less than 500).
4. Extract the unique `resource_id`s that have experienced at least one such violation.
5. Save these unique `resource_id`s, sorted alphabetically, to `/home/user/violations.txt` (one resource ID per line).

You must complete this entirely via the terminal using Python and SQLite.