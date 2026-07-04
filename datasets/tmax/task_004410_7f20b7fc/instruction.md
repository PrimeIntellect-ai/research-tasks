You are an operations engineer tasked with triaging an incident.

We have a data processing bash script in a local Git repository at `/home/user/data_processor`. The script `process_logs.sh` takes a file containing one integer per line and prints their sum.

Recently, our pipelines started hanging indefinitely. We suspect a recent commit introduced a bug that causes the script to infinite loop on a specific integer input.

Your task:
1. Write a fuzzer or test loop to test integers from 1 to 2000 to find the specific integer that causes `./process_logs.sh` to hang (run for more than 1 second).
2. Save this specific integer to `/home/user/hanging_input.txt`.
3. Use `git bisect` to find the commit hash that introduced this bug. Save the full commit hash to `/home/user/bad_commit.txt`.
4. Fix the infinite loop bug in `process_logs.sh` on the `main` branch so that the script correctly computes the sum for all inputs, including the one that previously caused a hang.
5. Commit your fix to the repository with the message "Fix infinite loop".

Note: The script should output exactly the sum of the numbers in the provided file, followed by a newline. Do not output anything else in the fixed script.