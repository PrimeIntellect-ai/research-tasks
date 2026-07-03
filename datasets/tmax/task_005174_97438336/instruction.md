You are the on-call engineer and have just been paged at 3 AM. A critical nightly Bash pipeline is failing and causing system instability.

The pipeline consists of a primary script located at `/home/user/pipeline/aggregate_metrics.sh`. It is designed to process a dataset `/home/user/pipeline/data.csv`.

There are three major issues you need to investigate and fix:
1. **Precision Loss**: The script is supposed to calculate the average of the values in the second column of `data.csv`. However, the current calculation is losing precision and returning an integer instead of a high-precision float. Fix the script to output the average with exactly 4 decimal places.
2. **"Linker" / Execution Error**: The script relies on a compiled helper utility called `metric_parser` located in the same directory. However, running the script throws a shared library error (`libcustom_math.so` not found). You need to configure the script so it can successfully find and link this dynamic library at runtime.
3. **Resource Leak on Cancellation**: The script simulates long-running tasks by spawning background processes. Currently, if the script is terminated early (e.g., via SIGTERM or SIGINT), these background processes are left running, causing a resource leak. Modify the script to correctly trap SIGTERM and SIGINT, and explicitly kill all its background child processes before exiting.

Your final goal is to successfully run `/home/user/pipeline/aggregate_metrics.sh` so that it completely processes the data without errors, does not leave background processes running if interrupted, and writes the correct average with exactly 4 decimal places to `/home/user/pipeline/result.txt`.

Do not change the filename of the output. The automated system will check `/home/user/pipeline/result.txt` for the exact numeric average, and will verify the trap handling.