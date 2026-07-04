I'm trying to debug a failing distributed build system. The build coordinator relies on a local caching service (`async-build-cache`), but the caching daemon crashed abruptly under heavy load during the last build. This caused two major issues:

1. **Database Corruption:** The cache daemon uses an append-only Write-Ahead Log (WAL) located at `/home/user/data/cache.wal`. The crash left the WAL truncated and corrupted. 
2. **Resource Leak (The Root Cause):** The caching daemon, which is an installed vendored package located at `/app/async-build-cache-1.0.0`, seems to have a bug where it leaks asyncio tasks/connections when build clients cancel their requests (e.g., due to timeouts). This led to file descriptor exhaustion and the crash.

I need you to fix the system by completing the following steps:

**Step 1: Timeline Reconstruction & Pcap Analysis**
You have access to the build logs at `/home/user/logs/build.log` and a network capture of the cache daemon traffic at `/home/user/logs/traffic.pcap`. 
Analyze these files to determine the exact `TXN_ID` of the last *fully acknowledged* transaction sent to the cache before the crash occurred.

**Step 2: WAL Database Recovery**
Write a Python script to parse `/home/user/data/cache.wal`. The WAL format is `[TIMESTAMP] [TXN_ID] SET <key> <value>`. 
Reconstruct the cache state into a valid JSON dictionary and save it to `/home/user/data/recovered.json`. 
*Crucial:* To avoid corrupted state, you must ONLY apply transactions up to and including the last acknowledged `TXN_ID` you found in Step 1. Discard any partial or unacknowledged transactions that follow it.

**Step 3: Fix the Resource Leak**
Inspect the source code of the vendored package at `/app/async-build-cache-1.0.0/async_build_cache/server.py`. Find and fix the asyncio cancellation leak. The server should cleanly terminate the connection task and release resources when a client disconnects unexpectedly. 

**Step 4: Verification**
Once you have fixed the package, reinstall it (`pip install -e /app/async-build-cache-1.0.0`).
Then, start the server (`python -m async_build_cache.server &`) and run the load test: `python /home/user/verify_throughput.py`. 
Your fix must allow the server to survive client cancellations and achieve a throughput of **>= 800 req/sec** without crashing.