You are a performance engineer called in to debug a severe resource leak in a Python asynchronous backend service. The service processes incoming network requests, but under heavy load with frequent client cancellations (disconnects), it leaks memory and file descriptors, eventually crashing. 

The service code is located in a local git repository at `/home/user/async_service`.

Your objectives are to investigate the repository, find the root cause, fix the code, and document your findings.

Here are your specific tasks:
1. **Git Forensics & Secrets Recovery:** The service requires a `config.json` file containing a `SECRET_KEY` to start. This file was accidentally committed to the repository in the past, then subsequently deleted. Search the git history, recover the `config.json` file, and place it in `/home/user/async_service/config.json`.
2. **Identify the Culprit Commit:** Using bisection or git log analysis, find the exact git commit hash that introduced the resource leak. The service was known to be perfectly stable in the initial commit. 
3. **Trace and Fix the Leak:** 
   - Start the service. You can use tools like `strace`, `pdb`, or simple load tests to observe what happens when a client connects and immediately disconnects.
   - You will find that an asynchronous background task is not properly handling client cancellation, leaving an orphaned task running forever. 
   - Modify `server.py` to correctly handle `asyncio.CancelledError` or correctly cancel the background task when the client disconnects.
4. **Add Assertion-based Validation:** In `server.py`, add a safety assertion in the main connection loop (after the client disconnects) that verifies the number of running background tasks does not continuously grow. Specifically, add an assertion that ensures the number of active background tasks for that specific connection handler goes to 0 upon disconnect.
5. **Generate a Resolution Report:**
   Create a file at `/home/user/resolution_report.json` with the following strict JSON structure:
   ```json
   {
       "secret_key": "<recovered_secret_key_value>",
       "culprit_commit": "<full_git_commit_hash>",
       "fixed_files": ["server.py"]
   }
   ```

To test your fix, you can write a short Python script to open and immediately close connections to the server on port 8888, observing if the active task count (printed by the server or viewable via `tracemalloc`/debugger) continues to grow.