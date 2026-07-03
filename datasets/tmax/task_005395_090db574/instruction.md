You are tasked with fixing a broken ETL ingestion server and building a data stratification script to feed it.

We have a custom, pre-vendored ingestion server located at `/app/vendored/etl-receiver-0.1.0/`. It provides an HTTP API to receive processed ETL data.
However, it currently has two issues you need to fix:
1. The package cannot be built/started because of a broken `Makefile` (it has a misconfigured environment variable that prevents it from starting as a non-root user).
2. We've noticed a severe bug during network failures: if an upstream client retries an upload by sending the same `Transaction-Id` header, the server appends the new records to the old ones in memory, resulting in duplicate records. You must patch the server logic to overwrite or clear the previous records for a given `Transaction-Id` on a retry.

Once you have fixed the ingestion server, start it so that it listens on `127.0.0.1:8080`. The server must require the Authorization token `Bearer super-secret-etl-token`. Read the source code of the server to understand how to configure the port and token (hint: look at its environment variables).

Next, you must write a multi-language data processing script (you can use Python, Ruby, or Node.js) to process a large multilingual dataset located at `/home/user/raw_events.csv`. 
The CSV has the following columns: `event_id`, `user_id`, `text_utf8`, `lang_code`, `engagement_score`.

Your script must:
1. Parse the CSV and handle the Unicode text correctly.
2. Group the records by `lang_code`.
3. Perform mathematical data sampling and stratification: Sort the records within each language group by `engagement_score` (numerically descending). If scores are tied, sort by `event_id` (lexicographically ascending).
4. Take exactly the top 10% of records from each language group (use a mathematical ceiling, e.g., if there are 11 records, take 2).
5. Send the stratified sample as a JSON array of objects to the ingestion server via a `POST /api/ingest` request. 
   - Set the `Transaction-Id` header to `TXN-INITIAL-LOAD`.
   - Set the correct `Authorization` header.

Your final state must be:
- The fixed `etl-receiver` server is running in the background, listening on `127.0.0.1:8080`.
- The server has successfully received and stored the stratified data from your script.

Keep the server running so our automated verifier can test the `/api/ingest` endpoint by issuing simulated retries and inspecting the processed mathematical samples.