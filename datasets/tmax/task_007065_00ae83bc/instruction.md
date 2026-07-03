You have just inherited an unfamiliar codebase located in `/home/user/worker_node`. 
The core of this system is a Python script named `processor.py` that processes incoming concurrent requests. The previous developer left a note saying: "The worker occasionally hangs indefinitely under high contention. I think it's a threading deadlock, but I couldn't reliably reproduce it or figure out which job gets stuck."

Your objectives are to:
1. **Reproduce the intermittent failure:** Write a stress-test script (in any language you choose) that executes `processor.py` or interacts with it to reliably trigger the deadlock.
2. **System tracing & Memory extraction:** Once the process is deadlocked (e.g., stuck waiting on a futex), capture a memory dump of the hung process. The application loads a unique tracking token into memory right before the deadlock occurs. This token is a string that starts with `STUCK_JOB_ID_` followed by a 16-character alphanumeric sequence. You must find this exact string in the memory dump.
3. **Root cause analysis & Patching:** Identify the cause of the deadlock in `processor.py`. Create a fixed version of the script and save it as `/home/user/worker_node/processor_fixed.py`. Your fixed version must not deadlock under any contention but must retain the exact same functionality and processing logic.

Finally, write your findings to `/home/user/solution.txt` in the following format:
```
TOKEN: STUCK_JOB_ID_<the_16_char_sequence>
DEADLOCK_CAUSE: <brief description of the lock ordering issue>
```

Ensure that:
- `/home/user/solution.txt` contains the correctly extracted token.
- `/home/user/worker_node/processor_fixed.py` exists, runs without syntax errors, and is completely free of deadlocks when heavily multithreaded.