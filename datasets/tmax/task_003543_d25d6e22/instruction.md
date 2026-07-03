You are a Database Reliability Engineer investigating an issue with our backup verification service. The service serves backup chain metadata (represented as a directed graph of incremental backups) over HTTP. 

We vendor a custom C application that handles this at `/app/backup_service-1.0`. It connects to an SQLite database located at `/home/user/metadata.db`.

Recently, a storage glitch corrupted the database's index (`idx_parent`), causing our graph projection queries (which use recursive CTEs and window functions) to return stale and incomplete backup chains. Furthermore, a recent botched patch to the C service left it unable to compile and failing to serve HTTP traffic correctly.

Your task is to fix the system and bring the service online:

1. **Fix the Vendored Package Build:** The `Makefile` in `/app/backup_service-1.0` is currently failing to link correctly. Identify the missing library flag and fix it so `make` completes successfully.
2. **Fix the C Service Bug:** The HTTP server in `/app/backup_service-1.0/server.c` has a bug where it abruptly closes the client connection before sending the JSON body. Find and fix this logic error.
3. **Repair and Optimize the Database:** The SQLite database `/home/user/metadata.db` has a table `backups(id INTEGER PRIMARY KEY, parent_id INTEGER, size INTEGER, backup_time DATETIME)`. 
   - You must fix the corrupted index by running a `REINDEX` or equivalent operation.
   - To support the analytical aggregation in the service, design and create a new covering index named `idx_opt` on `(id, parent_id, size, backup_time)`.
4. **Run the Service:** Start the compiled service. It is designed to listen on `127.0.0.1:8080`.

The service must correctly respond to HTTP GET requests at `/chain?id=<node_id>` with a JSON array of the backup chain, including a computed `cumulative_size` calculated via window functions in the C code's SQL query. Leave the service running in the background when you are finished.