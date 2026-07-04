You are a data engineer responsible for fixing a broken ETL pipeline. Recently, our primary SQLite data warehouse (`/app/warehouse.db`) experienced a critical index corruption, causing it to return "stale" transaction rows that break downstream graph analytics. 

An automated incident response system recorded a voice alert with the exact parameters of the corruption. This audio file is located at `/app/incident_alert.wav`.

Your objectives are:

1. **Information Extraction**: Transcribe `/app/incident_alert.wav` to discover the exact epoch timestamp threshold. Transactions older than this threshold are considered "stale" and must be rejected.

2. **ETL Filter Construction**: Write a Python script at `/home/user/etl_filter.py`. 
   - It must take a single command-line argument: the path to a JSON file containing an ETL payload (representing a transaction).
   - It must read the JSON file, inspect the `timestamp` field, and evaluate it against the threshold you discovered. 
   - It must print exactly `ACCEPT` to stdout if the transaction is fresh (timestamp >= threshold) and structurally valid, or `REJECT` if it is stale (timestamp < threshold) or malformed.
   - We will test your script against two hidden directories: a corpus of valid incoming payloads, and an adversarial corpus of stale/corrupted payloads.

3. **Graph Analytics Query**: The SQLite database `/app/warehouse.db` represents a financial graph. It contains `users` (nodes) and `transactions` (directed edges). 
   - Analyze the schema of `/app/warehouse.db`.
   - Write a script `/home/user/graph_query.py` that queries this database.
   - Your query must dynamically filter out any stale transactions using the threshold from the audio alert (simulate parameterized query construction).
   - Calculate the "in-degree" centrality for all users (the count of valid, non-stale incoming transactions to each user).
   - Write the `user_id` of the top 3 users with the highest in-degree, sorted descending, comma-separated on a single line, to `/home/user/top_users.txt`.

Ensure your filter script strictly outputs only `ACCEPT` or `REJECT` to stdout, as it will be used in an automated UNIX pipeline.