**Urgent 3 AM Page: Process Limit Exhaustion Incident**

You are the on-call engineer. At 3:00 AM, PagerDuty alerts you that our main data ingestion server is critically low on resources, hitting its maximum process limit (`ulimit -u`). 

After a preliminary investigation, the operations team found that a background processing script, `/home/user/worker.sh`, is hanging indefinitely on certain inputs. The parent service spawns hundreds of these workers asynchronously, and when they hang, they accumulate like leaked goroutines, eventually exhausting system process limits.

Your task is to debug this script, fix the root cause, and establish testing to prevent recurrence.

**The Buggy Script (`/home/user/worker.sh`):**
This script calculates a signal decay until it drops below a threshold (0.01). However, due to a bug related to numerical precision loss, certain inputs cause the calculation to stagnate, resulting in an infinite loop.

**Your Objectives:**

1. **Fix the Formula Implementation:**
   - Identify the precision loss bug in `/home/user/worker.sh`.
   - Create a corrected version at `/home/user/worker_fixed.sh`.
   - The fixed version must logically perform the same decay operation (multiplying by 0.5) but correctly terminate when the value drops below 0.01 without getting stuck.

2. **Regression Test Construction:**
   - Write a regression test script at `/home/user/regression.sh`.
   - This script must run `/home/user/worker_fixed.sh` with the specific input `1.0`. 
   - It should enforce a 2-second timeout using the `timeout` command.
   - If the worker completes successfully within the timeout, `regression.sh` must exit with `0`. If it hangs or fails, it must exit with `1`.

3. **Fuzz Testing:**
   - Write a fuzzer at `/home/user/fuzz.sh`.
   - The fuzzer should generate 50 random floating-point numbers between `0.0` and `10.0`.
   - It must execute `/home/user/worker_fixed.sh` against each generated number with a 1-second timeout.
   - The fuzzer must exit with `0` if all 50 runs complete successfully within the timeout, or exit with `1` if any run hangs.

**Environment details:**
- You only have access to standard Linux utilities (`bash`, `awk`, `bc`, `timeout`, etc.).
- The initial script `/home/user/worker.sh` has already been created for you (see system state).

Please proceed with diagnosing the error, fixing the code, and writing the validation scripts.