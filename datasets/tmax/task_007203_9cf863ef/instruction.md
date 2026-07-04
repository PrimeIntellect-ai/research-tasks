You are an operations engineer triaging an issue with a system metric calculation pipeline. A cron job failed overnight because the input log file was corrupted and a configuration file went missing.

Your task is to manually recover the data, fix the environment, and successfully run the metric calculation script using Bash and standard Linux tools.

Here are the requirements:
1. The raw log file is located at `/home/user/raw_logs.txt`. It contains chronological system events but has been corrupted with lines containing binary/non-ASCII garbage.
2. Filter out *all* lines containing non-ASCII characters from `/home/user/raw_logs.txt`. 
3. The original events were shuffled due to a log aggregation error. Sort the remaining valid, clean lines chronologically (earliest to latest) based on the ISO8601 timestamp in the first column.
4. Save the completely clean and sorted logs to `/home/user/clean_logs.txt`.
5. The calculation script `/home/user/process.sh` is failing. It expects a specific configuration file to exist, but the file was accidentally deleted. Read the script or trace its system calls (e.g., using `strace`) to discover the expected configuration file path.
6. Create the missing configuration file at the exact path the script expects. The file must be valid Bash and contain a single variable assignment: `FACTOR=3`.
7. Once the logs are clean, sorted, and the configuration file is restored, execute `/home/user/process.sh`. It will read `/home/user/clean_logs.txt` and output the final calculated mathematical result to `/home/user/answer.txt`.

Your final state will be evaluated by checking the contents of `/home/user/clean_logs.txt`, the presence of the correct configuration file, and the final integer value in `/home/user/answer.txt`.