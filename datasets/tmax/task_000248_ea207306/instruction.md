You are a performance engineer profiling a data processing pipeline. 

The main data processing script, located at `/home/user/data_pipeline/process.sh`, processes an event log `/home/user/data_pipeline/events.log`. It reads each event and attempts to trace its reference chain to the end (where `REF` is `NONE`). 

However, the pipeline is currently failing. When run, `process.sh` hangs indefinitely and consumes excessive CPU and memory until it crashes. Your investigation suggests there might be cyclic references in the data causing infinite recursion or an infinite loop.

Your task is to:
1. Use system call tracing tools (like `strace`) or bash debugging (`bash -x`) on the script to confirm the nature of the hang.
2. Fix the `/home/user/data_pipeline/process.sh` bash script. You must modify it so that it keeps track of visited events during a trace to detect cycles.
3. If a reference chain naturally terminates (reaches `NONE`), the script should output: `<START_ID> terminates normally`
4. If a reference chain contains a cycle (visits the same event ID twice in the same chain), it should immediately stop tracing that chain and output: `<START_ID> cycle detected`
5. The script must process every event in `events.log` as a starting point, one by one.
6. Run your fixed script and redirect the final standard output to `/home/user/data_pipeline/output.txt`.

Ensure your fixed script is written purely in Bash. Do not rewrite the logic in Python or Perl, though you may use standard coreutils (grep, awk, etc.) inside the Bash script.

The final verification will check the exact contents of `/home/user/data_pipeline/output.txt`. Ensure the output strictly follows the format specified above, with exactly one line per starting event ID in the order they appear in `events.log`.