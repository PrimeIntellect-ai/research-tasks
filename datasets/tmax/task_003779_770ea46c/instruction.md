You are a DevOps engineer tasked with debugging a nightly log processing job. 

A Python script located at `/home/user/process_logs.py` is designed to parse an access log file and convert it into a JSON Lines format. However, the script is crashing and failing to process the log file `/home/user/access.log`.

Your investigation suggests that the script fails because of a single malformed log line somewhere in the `access.log` file, which contains thousands of entries.

Your task is to:
1. Isolate the specific log line that is causing the script to crash. Use delta debugging, bisection, or trace analysis to find it.
2. Save the exact, unmodified text of this single malformed log line to a file named `/home/user/buggy_line.txt` (without any trailing newlines unless present in the original, just the line string itself).
3. Modify `/home/user/process_logs.py` so that it handles malformed lines gracefully. Specifically, if a line does not split into exactly 5 components (IP, timestamp, method, path, status) using the `" - "` delimiter, the script should silently skip that line and continue processing the rest of the file.
4. Run your fixed script to process `/home/user/access.log` and output the results to `/home/user/output.jsonl`. 

The original script is invoked like this:
`python3 /home/user/process_logs.py /home/user/access.log /home/user/output.jsonl`

Ensure your final `output.jsonl` contains all the valid parsed logs and that the script completes with a 0 exit code.