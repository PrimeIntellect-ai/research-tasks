A critical long-running service, `memory_tracker`, has been exhibiting memory leak symptoms. To make matters worse, a junior engineer accidentally deleted the service's allocation log (`/home/user/alloc.log`) while trying to free up disk space. The service is still running in the background.

Your task is to investigate and fix the memory leak:

1. **Deleted File Recovery**: The `memory_tracker` process is still running and holds the file descriptor for the deleted log open. Find the process, recover the contents of the deleted log file from the `/proc` filesystem, and save the recovered log to `/home/user/recovered.log`.
2. **Query Result Debugging**: Parse `/home/user/recovered.log`. The log format contains lines like `ALLOC <id> <address>` and `FREE <id> <address>`. Identify all allocation IDs that were NEVER freed. Write these leaked IDs to `/home/user/leaked_ids.txt` (one integer ID per line, sorted in ascending numerical order).
3. **Assertion-Based Validation & Code Fix**: Inspect the source code at `/home/user/memory_tracker.c`. Identify why certain allocations are not being freed. Fix the logic inside the loop to ensure every allocated pointer is freed. To ensure safety, add an assertion (`assert(ptr != NULL);`) immediately before your newly added `free()` call. You will need to ensure `<assert.h>` is included if not already present.
4. **Recompile**: Recompile the fixed source code using the command: `gcc /home/user/memory_tracker.c -o /home/user/memory_tracker_fixed`. 

Note: You do not need to kill or restart the originally running background process. Just compile the fixed binary to the specified path.