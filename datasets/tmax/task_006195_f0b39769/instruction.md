You are a cloud architect migrating a legacy VM system to a new containerized infrastructure. The legacy system boot sequence is simulated by a provided script at `/home/user/mock_qemu.py`. 

Previous automated migration attempts failed because the automation script sent the migration command before the VM's VNC service was fully initialized (similar to a missing `After=` dependency in systemd). 

Your task is to write an idempotent Python script that robustly automates this interactive process.

Create a Python script at `/home/user/start_services.py` that does the following:
1. **Idempotency Check**: First, check if the file `/home/user/migration.log` exists and contains the exact line `STATUS: [SUCCESS] VM state exported`. If it does, your script should immediately exit with code 0 without launching the mock VM.
2. **Process Supervision**: Spawn the `/home/user/mock_qemu.py` process. 
3. **Expect-like Synchronization**: Read the output of the process. You must wait until the exact string `[INFO] VNC server running on 127.0.0.1:5900` is printed by the mock VM. Do not send any commands before this line appears.
4. **Interactive Automation**: Once the VNC server is ready, send the command `MIGRATE\n` to the process's standard input.
5. **Logging**: The process will respond with a final status line. Capture this line and write it to `/home/user/migration.log` in the format: `STATUS: <final_line_here>`.

Ensure your Python script relies on standard libraries (e.g., `subprocess`) to interact with the mock VM. Ensure the script closes cleanly after the migration is complete.