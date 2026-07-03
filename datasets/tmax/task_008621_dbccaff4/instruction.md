You are tasked with debugging a long-running C service, `metrics-daemon`, which is suffering from severe memory leaks and data loss under high load.

The repository is located at `/home/user/metrics-daemon`. 

Here is what we know:
1. **Memory Leak**: The daemon leaks memory when it encounters malformed requests. A previous developer created a test payload that reliably triggered this leak, but accidentally deleted it in a recent commit.
2. **Data Loss (Concurrency)**: Under heavy concurrent load, the daemon drops some metrics. We suspect a race condition in the queue implementation (`queue.c`).
3. **Investigation**: We need to know exactly when the memory leak was introduced to audit other projects.

**Your Objectives:**
1. **Recover the Payload**: Inspect the Git history of `/home/user/metrics-daemon` and recover the deleted file named `bad_payload.txt`. Place the recovered file at `/home/user/metrics-daemon/bad_payload.txt`.
2. **Identify the Culprit**: Find the exact Git commit hash that *introduced* the memory leak in the parser logic. Write this full commit hash to a file named `/home/user/leak_commit.txt`.
3. **Fix the Memory Leak**: Modify `parser.c` to fix the memory leak. Ensure that all allocated memory is properly freed when invalid formats are encountered.
4. **Fix the Race Condition**: Modify `queue.c` to fix the race condition that causes metrics to be dropped or the linked list to become corrupted. Ensure proper locking mechanism is used.
5. **Verify**: Ensure the code compiles cleanly using the provided `Makefile` (`make`). The resulting binary should not leak memory when processing `bad_payload.txt` and should safely handle concurrent enqueue operations.

Do not change the function signatures or the overall architecture. Just fix the bugs.