You are an engineer tasked with diagnosing why a custom storage monitoring pseudo-service fails to start. 

The service uses a wrapper script `/home/user/start_service.sh` that simulates systemd's behavior by running an initialization script (`/home/user/setup_env.sh`) followed by the main C daemon (`/home/user/monitor`).

Currently, the service fails to start correctly. There are two underlying issues:
1. **Idempotency Failure**: The initialization script `/home/user/setup_env.sh` prepares mount directories based on an internal list. It is failing because the environment is already partially set up, and the script is not strictly idempotent. 
2. **Segmentation Fault**: The main daemon code `/home/user/monitor.c` reads a mock fstab file (`/home/user/user_fstab`) to check simulated disk quotas. It crashes when parsing this file due to unhandled edge cases in the file formatting (like blank lines).

Your task is to:
1. Modify `/home/user/setup_env.sh` so that it is completely idempotent (it must succeed whether the directories already exist or not).
2. Fix the C program `/home/user/monitor.c` so that it safely parses `/home/user/user_fstab`, ignoring any empty or blank lines, without crashing.
3. Recompile the C program: `gcc -o /home/user/monitor /home/user/monitor.c`
4. Run the wrapper script and direct its output to a log file: `/home/user/start_service.sh > /home/user/service_status.log 2>&1`

**Success Criteria:**
The file `/home/user/service_status.log` must be created by the wrapper script and end with the exact text outputted by the fixed, successfully completed monitor daemon. The script and daemon must exit with a `0` status code.