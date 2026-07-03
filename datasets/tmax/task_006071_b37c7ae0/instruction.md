We are trying to automate the testing of our backup restores. We have a local mock database service and a restore script, but our automation constantly fails because the restore script is executed before the database mock has fully initialized. We need you to write a robust process manager in Python to fix this dependency issue.

The following files exist on the system:
1. `/home/user/db_mock.py`: A database mock service. When executed, it simulates a startup sequence, and after a few seconds, it creates a readiness file at `/home/user/db_ready.sock`. It runs indefinitely until it receives a SIGTERM, at which point it cleans up the socket file and exits.
2. `/home/user/run_restore.py`: A script that performs the simulated restore. It instantly checks for the existence of `/home/user/db_ready.sock`. If the socket is missing, it crashes with a connection error. If present, it prints a success code to standard output.

Your task is to create a Python script at `/home/user/restore_manager.py` that reliably orchestrates this process. The script must:
1. Be written in Python 3.
2. Start the `/home/user/db_mock.py` process in the background.
3. Robustly poll/monitor for the creation of `/home/user/db_ready.sock`, implementing a sensible timeout (e.g., 10 seconds) to prevent infinite hanging.
4. Once the socket exists, execute `/home/user/run_restore.py`.
5. Capture the standard output of `/home/user/run_restore.py` and write it exactly as-is to a new file at `/home/user/restore_success.log`.
6. Terminate the `db_mock.py` process cleanly (send SIGTERM) and wait for it to exit, ensuring the socket is cleaned up.
7. The script must be idempotent and handle errors gracefully (e.g., if the socket already exists from a previous crashed run, or if the process fails to start).

Run your script to ensure it completes successfully and generates the `/home/user/restore_success.log` file. Leave the system in a clean state with no dangling background processes.