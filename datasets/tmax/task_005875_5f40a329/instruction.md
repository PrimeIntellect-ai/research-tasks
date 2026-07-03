You are a DevOps engineer investigating a recent critical failure in a Python-based transaction processing daemon. The service crashed due to a concurrency issue, leaving behind some logs and a memory dump. 

Your tasks are to fix the bug in the application code and extract the trapped transaction IDs from the memory dump.

Here is the setup located in `/home/user/app`:
1. `/home/user/app/processor.py` - The Python script containing the concurrency bug. It uses two locks (`lock_a` and `lock_b`). 
2. `/home/user/app/app.log` - The application log showing the last actions before the crash.
3. `/home/user/app/memory.dmp` - A simulated raw memory dump file (binary) created at the time of the crash.

**Step 1: Code Fix**
Analyze `/home/user/app/processor.py`. There is a classic deadlock caused by inconsistent lock acquisition order between the `process_x` and `process_y` functions. Modify `/home/user/app/processor.py` to fix this deadlock. Ensure that BOTH functions always acquire `lock_a` first, followed by `lock_b`. Do not change the function signatures or the core print statements.

**Step 2: Log and Memory Analysis**
Read `/home/user/app/app.log` to identify the names of the two threads that deadlocked (they will be the threads that started a transaction but never finished it). 
Then, analyze the `/home/user/app/memory.dmp` binary file. Somewhere in this file, the application logged the active transaction IDs in plain text strings formatted as `[Thread-Name] TXN_ID: <alphanumeric_id>`. 
Extract the transaction IDs specifically belonging to the two deadlocked threads.

**Step 3: Reporting**
Create a file at `/home/user/solution.txt`. Write the two deadlocked transaction IDs into this file on a single line, separated by a comma, in alphabetical order. 

Example format for `/home/user/solution.txt`:
TXN_1A2B3C, TXN_9F8E7D