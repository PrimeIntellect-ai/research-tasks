You are a data engineer building a lightweight ETL pipeline and serving its results via an HTTP API, using only Bash and core Unix tools. 

You need to complete the following multi-stage workflow:

1. **Fix and Install Vendored Package**: 
   We require `datamash` for performant numerical aggregations. The source code for `datamash-1.8` is pre-vendored at `/app/datamash-1.8`. However, a previous developer accidentally broke the `Makefile.in` (there is a typo in the `bin_PROGRAMS` or install target where it tries to build/install a binary called `datamas` instead of `datamash`). 
   - Locate the typo in `/app/datamash-1.8/Makefile.in`.
   - Fix it so the binary is correctly named `datamash`.
   - Run `./configure --prefix=/usr/local`, compile, and install it.

2. **Develop the ETL Pipeline**:
   Write a Bash script at `/home/user/etl.sh` that processes a CSV file located at `/home/user/transactions.csv`.
   - The CSV has headers: `tx_id,user_id,amount`.
   - Use your installed `datamash` (or a combination of `awk` and `datamash`) to group by `user_id` and calculate the sum of `amount`.
   - **Critical Accuracy Requirement:** The `user_id` column contains 19-digit integers (e.g., Twitter Snowflake IDs). You must ensure that your pipeline does not silently convert these large integers into floats or scientific notation (a common issue when tools ingest empty fields as NaN or cast large numbers). The output must preserve the exact 19-digit string.
   - The script must output the aggregated data as a valid JSON object where keys are the precise `user_id` strings and values are the summed `amount`s (as numbers). E.g., `{"1234567890123456789": 150.50}`.

3. **Serve via HTTP API**:
   Create a Bash script at `/home/user/server.sh` that uses `nc` (netcat) or `socat` to act as an HTTP server.
   - It must listen on **127.0.0.1:9090**.
   - When it receives any HTTP GET request, it should execute `/home/user/etl.sh` and return the JSON output.
   - The response must include standard HTTP headers: `HTTP/1.1 200 OK` and `Content-Type: application/json`.
   - Start this server in the background so it remains active.

Ensure the service is actively listening on port 9090 and correctly formatted JSON is returned when queried.