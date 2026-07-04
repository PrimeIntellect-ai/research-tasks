You are a FinOps analyst responsible for optimizing cloud costs. We have a custom network traffic cost analyzer written in C++ that processes network usage logs from our QEMU virtual machines. 

Currently, our cost reporting pipeline is broken due to a few issues:
1. **Tool Bug**: The C++ analyzer source code located at `/app/netcost-1.2.0/` has a logic bug that causes it to under-report costs (it seems to be missing the last byte of every stream). 
2. **Pipeline Script**: The CI/CD pipeline script `/home/user/pipeline/run_cost.sh` is supposed to run automatically (like a cron job) in a restricted environment. However, it currently writes its output to the wrong location due to relying on a relative directory path, and it fails to find the analyzer tool due to `PATH` differences.
3. **Directory Structure**: The script expects VM logs to be available at `/home/user/vm-logs/`, but the QEMU logs are actually stored in `/tmp/qemu-vms/`.

Your tasks are:
1. Inspect and fix the C++ code in `/app/netcost-1.2.0/` so that it correctly processes the entire input stream. Build the corrected executable and place it at `/home/user/bin/netcost`. Ensure it reads from standard input and writes the computed integer cost to standard output.
2. Fix `/home/user/pipeline/run_cost.sh` so that it successfully executes `/home/user/bin/netcost` even in an environment with an empty `PATH`. 
3. Modify the script so that its output is always written to the absolute path `/home/user/reports/cost.out`, regardless of which directory the script is executed from.
4. Set up the correct directory structure by creating a symbolic link from `/tmp/qemu-vms/` to `/home/user/vm-logs/` so the script can find the logs.

You must ensure that the final compiled tool at `/home/user/bin/netcost` perfectly matches the expected cost calculation logic for any valid input string.