You are tasked with investigating and fixing a long-running C++ key-value service that has been failing in production. The service is vendored locally under `/app/vendored_kv`. It currently fails to compile, crashes on startup due to a corrupted Write-Ahead Log (WAL), and suffers from a severe memory leak when serving requests.

Your objectives are to repair the package, recover the data, fix the leak, and bring the service back online.

**Step 1: Fix the Vendored Package Setup**
The source code for the custom key-value server is located in `/app/vendored_kv`. Currently, running `make` fails because of a missing compilation flag required for multi-threading. Diagnose the build error and fix the `Makefile` so the application compiles successfully into an executable named `kv_server`.

**Step 2: Database Recovery**
The server's data directory is located at `/app/data/`. When you attempt to run the compiled server (`./kv_server /app/data/server.wal 9090`), it will panic and exit because the WAL file (`server.wal`) is corrupted. 
Analyze the WAL file (which is a text-based append-only log) and the server's crash traceback. A recent incomplete transaction corrupted the file. Recover the database by safely excising the corrupted transaction without losing the preceding valid data. The server must be able to boot cleanly and load the existing valid keys.

**Step 3: Git Forensics & Authentication**
The server requires an Authentication token to process client commands, but the token is not documented and was recently refactored out of the default configuration. Use the local git repository in `/app/vendored_kv` to perform git forensics. Find the hardcoded administration token that was used prior to the recent "Security refactor" commit. 

**Step 4: Fix the Memory Leak**
Production logs indicate that the server's memory usage balloons rapidly when clients issue `GET` requests. Use standard tools (like `valgrind` or manual code review) on the C++ source code to identify and patch the memory leak in the request handling logic. 

**Step 5: Run the Service**
Start the fixed server as a background process. It must:
- Listen on `127.0.0.1:9090`.
- Use the recovered WAL file at `/app/data/server.wal`.

**Step 6: Create a Reproducible Example**
To prove the system is stable, write a minimal bash script at `/home/user/repro.sh` that uses `nc` (netcat) to communicate with your running server. The script should:
1. Connect to the server.
2. Send the `AUTH <token>` command.
3. Send a `SET testkey testval` command.
4. Send 50 `GET testkey` commands in a loop.
Ensure your script exits cleanly.

Do not use any external network resources to solve this task. Everything you need is contained within `/app/vendored_kv` and the system's standard utilities.