You are a data engineer tasked with building a C-based ETL microservice. You need to extract customer records from a local SQLite database, mask sensitive information, format the data as a JSON array, and serve it via a custom TCP service.

Here are the requirements:

1. **Fix the Vendored JSON Library**: 
   We rely on `cJSON` for JSON manipulation. A vendored version is located at `/app/cJSON-1.7.15`. However, the build is currently failing due to a configuration error in its `Makefile` introduced during vendoring. Find the perturbation, fix it, and build the shared library (`libcjson.so`).

2. **Database Specifications**:
   A SQLite database is located at `/home/user/data.db` (you may assume it will be created and populated before your service runs). It has a table named `customers`:
   `CREATE TABLE customers (id INTEGER PRIMARY KEY, name TEXT, email TEXT, credit_card TEXT);`

3. **ETL & Masking Logic**:
   Write a C program at `/home/user/etl_server.c` that connects to this database and extracts all records.
   You must apply the following masking rules:
   - `email`: Retain the first character, replace the rest of the local part with `***`, and keep the domain. (e.g., `alice@example.com` becomes `a***@example.com`).
   - `credit_card`: Replace all digits except the last 4 with `X` (e.g., `1234567812345678` becomes `XXXXXXXXXXXX5678`).
   - Format the extracted, masked data into a JSON array of objects using the fixed `cJSON` library. 

4. **Service Protocol**:
   Your C program must run as a daemon or foreground process listening on `127.0.0.1:8000` via raw TCP.
   When a client connects and sends the exact string `RUN_ETL SECRET_TOKEN_42\n`, your service must:
   - Perform the extraction and masking (validation gate: do not return unmasked credit cards).
   - Send the generated JSON array back to the client.
   - Immediately follow the JSON payload with `\nEND\n` on a new line.
   - Close the client connection.
   - If an invalid token or command is sent, send `ERROR\n` and close the connection.

Ensure your server is compiled with `-lsqlite3` and the linked `cJSON` library. Leave the server running in the background listening on port 8000 when you are finished.