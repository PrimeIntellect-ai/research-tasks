You are an IT support technician assigned to resolve an escalated ticket (Ticket #8824). 

**Issue Description:**
The data engineering team has a bash-based batch processing job that calculates checksums for files containing arrays of integers. However, the job intermittently fails or outputs corrupted (empty) checksums for certain files. The team suspects a dependency conflict between different versions of their logging utilities causing a state corruption during intermittent edge cases (specifically, when the sum of a file's numbers happens to be a multiple of 7).

**Environment:**
- The working directory is `/home/user/ticket_system/`.
- The main entrypoint is `/home/user/ticket_system/calc_checksums.sh`.
- The data files are located in `/home/user/ticket_system/data/`.
- Library scripts are in `/home/user/ticket_system/lib/`.
- Container logs showing past intermittent failures are in `/home/user/ticket_system/logs/error.log`.

**Your Task:**
1. Diagnose the intermittent failure in `/home/user/ticket_system/calc_checksums.sh` and its dependencies.
2. Fix the scripts so that dependency conflicts are resolved and the mathematical checksum (`MATH_TMP`) is never corrupted.
3. Once fixed, execute the script against all data files: 
   `./calc_checksums.sh data/batch_*.txt > /home/user/ticket_system/final_results.txt` (Make sure to run this from `/home/user/ticket_system/`).
4. Ensure the output format in `final_results.txt` contains exactly the standard output (not standard error) in the format `data/batch_X.txt: SUM`.

Your success will be verified by an automated test checking the exact contents of `/home/user/ticket_system/final_results.txt`. Do not output any logs to standard output in your final run; all logs should be directed to standard error as originally intended.