You are an observability engineer trying to fix a faulty custom metric collection setup. 

There is a C program located at `/home/user/emitter.c`. This program is designed to perform a health check and write the result to a log file. Currently, it hardcodes the output file as `"health.log"` in the current working directory. Because this program is run by various automation scripts (and eventually cron jobs), the output file ends up scattered across different directories depending on the current working directory of the caller.

Your task is to:
1. Modify `/home/user/emitter.c` so that it retrieves the output directory from the `METRICS_OUT_DIR` environment variable. 
2. The program must construct the full path by appending `/health.log` to the directory path specified by `METRICS_OUT_DIR`.
3. If the `METRICS_OUT_DIR` environment variable is not set, the C program must print an error message to standard error and exit with a non-zero exit code (e.g., exit code 1).
4. If it successfully opens the file, it should append the string `"status=OK\n"` to it and exit with code 0.
5. Create an idempotent bash script at `/home/user/setup_observability.sh` that performs the following actions:
   a. Compiles `/home/user/emitter.c` to an executable named `/home/user/emitter`.
   b. Creates the target metrics directory `/home/user/dashboard_metrics` if it does not already exist.
   c. Generates an executable wrapper script at `/home/user/run_emitter.sh`. This wrapper script must export the `METRICS_OUT_DIR` variable as `/home/user/dashboard_metrics` and execute the compiled `/home/user/emitter` program.
   d. The `setup_observability.sh` script must be idempotent (safe to run multiple times without causing errors or appending duplicate code to the wrapper script).

Ensure that all scripts you create are marked as executable. You can run `./setup_observability.sh` and then `./run_emitter.sh` to test your solution.