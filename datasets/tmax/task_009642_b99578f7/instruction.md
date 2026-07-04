You are an IT support technician investigating an intermittent crash in a legacy backend system. A scheduled Python script (`/home/user/run_batch.py`) has been failing overnight. It loops through a list of user IDs in `/home/user/users.txt` and invokes a C utility called `legacy_auth` for each ID.

When the script encounters certain user IDs, the C utility crashes, halting the entire batch process. The crash is known to be caused by a 32-bit signed integer overflow in the C code (`/home/user/legacy_auth.c`), but the exact inputs triggering it haven't been documented.

Your objectives:
1. **Reproduce and Analyze the Crash:** Use core dumps and an interactive debugger (e.g., `gdb`) to capture the crash. Identify the exact user ID from `/home/user/users.txt` that first triggers the segmentation fault during the execution of `run_batch.py`.
2. **Document the Crashing ID:** Write the precise user ID that caused the crash into `/home/user/crashing_id.txt`.
3. **Write a Fix Script:** We cannot modify the legacy C binary yet, but we need to bypass the issue. Write a Python script at `/home/user/filter_users.py` that reads `/home/user/users.txt` and filters out ANY user IDs that would trigger the signed integer overflow in `legacy_auth.c` (you can inspect the C source to determine the exact multiplier and logic). Save the safe user IDs (one per line, preserving original order) to `/home/user/safe_users.txt`.

Ensure your python script dynamically applies the math logic to determine safety (assuming standard 32-bit signed integer limits) rather than hardcoding the specific crashing ID you found.