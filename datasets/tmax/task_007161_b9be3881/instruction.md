You are acting as a container specialist managing a legacy payment microservice. The service dumps unstructured logs into a single file, and you need to process these logs, secure the output, and implement a basic rotation mechanism.

Your tasks are as follows:

1. **Log Parsing (Python):** 
   Write a Python script at `/home/user/process_logs.py`. It must read the raw log file located at `/home/user/raw_logs/payment.log`. 
   The script should find all lines containing both the exact string `[ERROR]` and the string `action="checkout"`. 
   From these lines, extract the `tx_id` value and the `reason` value.
   The script must write the extracted information to `/home/user/secure_logs/error_summary.log` in the exact format:
   `TX_ID: <tx_id> | REASON: <reason>`
   (One entry per line, in the same order they appear in the original log).

2. **Permissions Management:**
   Because these logs contain sensitive transaction IDs, you must ensure strict permissions:
   - The directory `/home/user/secure_logs/` must have `0700` permissions.
   - The file `/home/user/secure_logs/error_summary.log` must have `0400` (read-only for the owner) permissions.

3. **Log Rotation (Bash):**
   Write a bash script at `/home/user/rotate_logs.sh` that performs a manual log rotation:
   - It should rename `/home/user/secure_logs/error_summary.log` to `/home/user/secure_logs/error_summary.log.1`.
   - It should create a new, empty `/home/user/secure_logs/error_summary.log`.
   - It must ensure the new file also has `0400` permissions, and the rotated file retains `0400` permissions.

4. **Execution:**
   - Run your Python script to generate the initial summary log.
   - Ensure permissions are set correctly.
   - Run your rotation bash script exactly once.

Note: The raw log file at `/home/user/raw_logs/payment.log` has already been created for you.