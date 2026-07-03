You are a support engineer tasked with recovering a failed data ingestion system and collecting diagnostics. The system processes a custom Write-Ahead Log (WAL) of financial transactions and forwards them to an upstream API, which then caches them in Redis. 

Recently, a bad deployment crashed the system, leaving behind a corrupted WAL file and a broken C ingestion service. Your goal is to repair the environment, fix the service, recover the data, and successfully ingest it into the running system.

System Environment (located in `/home/user/app`):
1. **Redis**: Needs to run on port 6379.
2. **Upstream API**: A Python Flask application located in `/home/user/app/api/server.py` that listens on port 5000.
3. **Ingester Service**: A C program located in `/home/user/app/ingester/ingester.c`.

Here is your diagnostic and recovery checklist:

1. **Environment & Secrets Recovery**: 
   The C ingester requires an environment variable `API_SECRET` to authenticate with the API. This secret was recently lost due to a bad configuration update, but the previous developers accidentally committed it to the git repository in `/home/user/app/ingester` at some point before deleting it. Find this secret in the git history and write it to `/home/user/app/config.env` in the format `API_SECRET=<secret_value>`.

2. **Compilation & Linker Repair**:
   The `ingester.c` file currently fails to compile due to missing headers and linker errors. Diagnose the compiler output, fix the C code (if necessary), and compile it into an executable named `ingester` in the same directory. You may need to install standard development libraries for HTTP requests (the code uses libcurl).

3. **Database (WAL) Recovery**:
   The ingester reads a binary file located at `/home/user/app/data/transactions.wal`. The WAL consists of sequential records. Each record has a strict format:
   - Magic Header: 4 bytes (always `0xDEADBEEF`)
   - Record Size: 4 bytes (unsigned integer, representing the size of the JSON payload)
   - Payload: <Record Size> bytes of JSON string.
   
   Due to a bug in the previous version, the WAL file became corrupted. Some records have an invalid "Record Size" (e.g., randomly huge numbers), causing the current `ingester.c` to attempt massive memory allocations and segfault. 
   Modify `ingester.c` to gracefully detect and skip corrupted records. A valid payload size will never exceed 1024 bytes. If a record is corrupt, the program should scan forward byte-by-byte until it finds the next valid `0xDEADBEEF` magic header and resume reading.

4. **Service Orchestration**:
   Start the Redis server and the Python API. You can launch them using the provided script `/home/user/app/start_services.sh`. Ensure they are communicating properly. Then, execute your compiled `ingester` program to process `transactions.wal` and send the recovered records to the API.

An automated diagnostic script will evaluate your success by calling the API's `/metrics` endpoint to check the percentage of recovered records. You must achieve a high recovery yield to pass.