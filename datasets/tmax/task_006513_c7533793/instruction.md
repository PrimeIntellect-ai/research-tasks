You are a Site Reliability Engineer (SRE) investigating intermittent downtime caused by a custom monitoring daemon hanging indefinitely. 

The daemon is written in Python (`/home/user/uptime_monitor/agent.py`) and uses a custom C library (`libmetrics.so`) for high-performance system metric querying via `ctypes`. Under high concurrency, the agent deadlocks, causing monitoring to fail.

Your tasks are:
1. **Fix the Build System**: The previous engineer started writing a fix but broke the `Makefile` located in `/home/user/uptime_monitor/Makefile`. When you try to run `make`, it fails with a linker error. Diagnose and fix the compiler/linker error so the shared library can build successfully.
2. **Diagnose the Deadlock**: Use a debugger (like `gdb`) to attach to a hanging instance of `python3 agent.py` (or analyze the code) to identify the root cause.
3. **Fix the Deadlock**: Modify `/home/user/uptime_monitor/libmetrics.c` to prevent the race condition/deadlock. Ensure all threads can query both CPU and Memory metrics safely under high contention. Ensure the fixed library builds successfully using `make`.
4. **Test**: Ensure that running `python3 /home/user/uptime_monitor/agent.py` completes successfully without hanging.
5. **Report**: Create a JSON file at `/home/user/resolution.json` with your findings. It must strictly follow this structure:
```json
{
  "linker_error_fixed": true,
  "deadlocked_functions": ["<name of C function 1>", "<name of C function 2>"],
  "fix_strategy": "<brief string explaining how you resolved the lock ordering>"
}
```
*Note: Sort the `deadlocked_functions` list alphabetically.*

All work should be done in `/home/user/uptime_monitor/`. Do not modify the Python script `agent.py`; your fixes should entirely be in the `Makefile` and `libmetrics.c`.