You are tasked with building a high-performance data anonymization and bulk-import service in C++ for our data science team. We have a legacy system that masks PII, but it is too slow for our current pipeline.

Here is your objective:

1. **Reverse Engineer the Legacy Masker:**
   You will find a stripped binary at `/app/legacy_masker`. It takes a single string argument (e.g., an Email or SSN) and prints a masked version of it. 
   Analyze this binary to determine its exact masking algorithm. You must implement this exact masking logic natively in your C++ service to achieve the required throughput.

2. **Develop the C++ Processing Service:**
   Write a C++ server that listens for raw TCP connections on `127.0.0.1:9090`. 
   The server must implement the following line-based protocol:
   - A client initiates a bulk load by sending: `BULK_LOAD\n`
   - The client then sends multiple lines of CSV data. The CSV format is: `id,name,email,ssn`.
   - The client signals the end of the data by sending the exact line: `EOF\n`
   
   Upon receiving `EOF\n`, your service must:
   - Apply the masking algorithm (reverse-engineered from the binary) to the `email` and `ssn` columns of all received rows.
   - Bulk-insert the processed records into a SQLite database located at `/home/user/anonymized.db`. The table must be named `users` with columns `(id INTEGER, name TEXT, email TEXT, ssn TEXT)`.
   - Send exactly `SUCCESS <number_of_rows_inserted>\n` back to the TCP client.
   - Keep listening for new connections.

3. **Pipeline Orchestration:**
   Ensure your C++ code is compiled with `-O3` to a binary named `/home/user/data_service`. 
   Run your service in the background so it is listening on port 9090 when the verification step begins. The database file `/home/user/anonymized.db` must be created and properly initialized with the `users` table before the server starts accepting data.

Constraints:
- Use only standard C/C++ libraries and `sqlite3` (you may install `libsqlite3-dev` if needed).
- The verifier will connect to `127.0.0.1:9090`, stream thousands of rows, and check both the TCP response and the final contents of `/home/user/anonymized.db`.