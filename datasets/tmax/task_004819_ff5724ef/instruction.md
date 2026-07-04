We are deploying a new configuration manager that receives ETL logs from remote edge devices. Due to network instability, the remote data transfer mechanism frequently retries, causing duplicate records to be sent to our endpoint. 

You need to build a lightweight C-based HTTP service that processes these incoming logs, deduplicates them, and maintains a rolling statistic of the configuration payload sizes.

We have pre-vendored a minimal third-party C HTTP library, `tinyhttp` (v1.0), located at `/app/vendored/tinyhttp`. However, the previous engineer reported that the library fails to compile out of the box on our system. You will need to identify the issue in the library's build configuration or source, fix it, and use the library to build your service.

Your task:
1. **Fix the Vendored Package:** Inspect `/app/vendored/tinyhttp`. Fix whatever is preventing it from compiling into a shared or static library (`libtinyhttp.a` or `libtinyhttp.so`).
2. **Develop the Service:** Create a C application at `/home/user/config_server.c` that uses `tinyhttp` to listen on `127.0.0.1:8080`.
3. **Regex Extraction & Deduplication:** 
   Implement a `POST /config` endpoint. The body will be plain text containing a log entry like: `[TXN:<txn_id>] SET <key>=<value> SIZE=<bytes>` (e.g., `[TXN:AB12] SET max_workers=5 SIZE=120`).
   Use POSIX regex (e.g., `regex.h`) to extract the `<txn_id>` (alphanumeric) and the `<bytes>` (integer).
   Maintain a history of seen `<txn_id>`s. If a `<txn_id>` has already been processed, ignore the request (this handles the duplicate records on retry).
4. **Rolling Statistics:**
   For every *unique* transaction, store the `<bytes>` value in a rolling window of size 5. 
   Implement a `GET /stats` endpoint that computes the average size of the elements currently in the rolling window (up to 5 elements). The response must be exactly formatted as `Average: <float>\n` (using `%.2f` precision).

Compile your service and start it in the background so it binds to `127.0.0.1:8080` and is ready to receive traffic.