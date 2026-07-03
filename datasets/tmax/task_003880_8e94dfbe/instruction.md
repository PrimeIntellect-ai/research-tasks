You are a monitoring specialist tasked with fixing and setting up a basic alert system for a simulated worker process. 

Currently, there is a C source file located at `/home/user/worker.c` that reads a sequence of metric values from `/home/user/metrics.dat` and prints logs to standard output. However, the threshold for generating critical alerts is hardcoded, and the downstream alert processing is missing.

Perform the following tasks:
1. Modify `/home/user/worker.c` so that the alert threshold is read from the environment variable `ALERT_THRESHOLD`. If the variable is not set, it should default to `80`. The program should parse the environment variable as an integer using standard C libraries. Do not change the existing format of the printed log messages.
2. Compile the updated C program to `/home/user/worker`.
3. Configure the environment by adding `export ALERT_THRESHOLD=85` to `/home/user/.bashrc`. 
4. Create a shell script at `/home/user/run_monitor.sh` that does the following:
   - Sources `/home/user/.bashrc` to ensure the environment variable is loaded.
   - Executes the compiled `/home/user/worker` binary.
   - Pipes the output of the binary into a text processing pipeline (using `grep`, `awk`, or `sed`).
   - The pipeline must filter only the lines starting with `CRITICAL:`, and reformat them to look exactly like this: `[ALERT] <rest of the message>`.
   - For example, if the binary outputs `CRITICAL: Value 90 exceeds threshold`, the pipeline should output `[ALERT] Value 90 exceeds threshold`.
   - The reformatted output must be redirected and saved to `/home/user/alerts.log`.
5. Execute the `/home/user/run_monitor.sh` script so that `/home/user/alerts.log` is generated.

Ensure that all file paths are exactly as specified and that permissions on `/home/user/run_monitor.sh` allow it to be executed.