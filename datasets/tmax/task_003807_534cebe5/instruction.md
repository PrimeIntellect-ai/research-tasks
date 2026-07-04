You are a DevOps engineer stepping in to fix a broken data processing pipeline. The previous engineer left abruptly, and the Go-based log ingestion service has been crashing. 

Here is what we know and have in the `/home/user/pipeline` directory:
1. `/home/user/pipeline/bin/logparser`: A compiled Go binary that processes our logs. It currently fails to run because of an environment misconfiguration (a missing environment variable). The previous engineer mentioned they hardcoded the required environment variable name in the binary itself before compiling.
2. `/home/user/pipeline/dumps/core.dump`: A memory dump taken right before the last crash. It contains the active `CLIENT_SECRET` that the system was using (it starts with the prefix `CS_` followed by exactly 10 alphanumeric characters, e.g., `CS_a1b2c3d4e5`).
3. `/home/user/pipeline/data/input.log`: The raw log data that needs to be processed.

Your tasks are:
1. **Binary Analysis**: Analyze the `/home/user/pipeline/bin/logparser` binary to find the exact name of the missing environment variable it expects.
2. **Memory Dump Analysis**: Extract the `CLIENT_SECRET` from the `/home/user/pipeline/dumps/core.dump` file.
3. **Pipeline Restoration**: Write a Go program at `/home/user/pipeline/recover.go` that reads `/home/user/pipeline/data/input.log` and writes ONLY the lines containing the `CLIENT_SECRET` to `/home/user/pipeline/data/output.log`. 
4. **Environment Repair**: Create a file named `/home/user/pipeline/env.txt` containing exactly two lines:
   - Line 1: The name of the missing environment variable found in the binary.
   - Line 2: The `CLIENT_SECRET` found in the memory dump.

Ensure your Go program compiles and runs successfully, producing the required `output.log`.