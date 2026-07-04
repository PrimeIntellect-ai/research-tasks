You are an edge computing engineer deploying a data processing pipeline to an IoT device. The device needs to receive over-the-air updates via Git, compile a C-based sensor parser, and manage the execution of this parser with automated restarts and log filtering.

Your objective is to implement the entire pipeline in `/home/user`. Do not use root privileges. 

Step 1: Data Source
There is a file at `/home/user/raw_data.txt` (which you must create for testing) with the following exact content:
1700000000 24.5
1700000005 88.1 ANOMALY
1700000010 23.9
1700000015 95.0 ANOMALY
1700000020 24.1

Step 2: Git Server Configuration
1. Initialize a bare Git repository at `/home/user/iot_update.git`.
2. Create a local clone of this repository at `/home/user/workspace`.

Step 3: The C Parser
In your clone (`/home/user/workspace`), write a C program named `parser.c`.
This program must:
1. Read lines from standard input in the format: `<UNIX_TIMESTAMP> <VALUE> [OPTIONAL_TAGS...]`
2. Parse the Unix timestamp.
3. Convert the timestamp to a local time string using the standard C library (`localtime`, `strftime` with format `%Y-%m-%d %H:%M:%S`). 
4. Print the formatted output to standard output as: `[YYYY-MM-DD HH:MM:S] <VALUE> [OPTIONAL_TAGS...]`
5. After processing all lines from standard input (EOF), the program must intentionally simulate a crash by exiting with status code `1` (this is to test our restart policy).

Step 4: The Supervisor and Text Processing Pipeline
In your clone, write a bash script named `supervisor.sh`. 
This script must:
1. Act as a process supervisor that runs in an infinite loop.
2. Inside the loop, it must execute the compiled `parser` binary, feeding it `/home/user/raw_data.txt` via standard input.
3. Crucially, the parser MUST be executed with the environment variables `TZ=Asia/Tokyo` and `LC_TIME=C` so that the timestamps are formatted in the Tokyo timezone.
4. The output of the parser must be piped through a text processing pipeline that:
   - Uses `grep` to filter OUT any lines containing the word `ANOMALY`.
   - Uses `awk` or `sed` to prepend the string `VALIDATED: ` to the remaining lines.
   - Appends the final output to `/home/user/processed.log`.
5. If the parser exits with code `1` (which it will), the supervisor must sleep for `2` seconds, append the exact string `RESTARTING PARSER` to `/home/user/processed.log`, and then restart the parser (loop again).
6. The script should be executable.

Step 5: The Git Hook
Configure a `post-receive` hook in the bare repository (`/home/user/iot_update.git/hooks/post-receive`).
When code is pushed, this hook must:
1. Checkout the latest code into a deployment directory at `/home/user/deploy` (create this directory if it doesn't exist).
2. Compile `parser.c` into an executable named `parser` inside `/home/user/deploy`.
3. Kill any currently running `supervisor.sh` processes to ensure a clean state.
4. Start `supervisor.sh` in the background (detached), routing its standard error to `/dev/null`.

Step 6: Deployment
Commit `parser.c` and `supervisor.sh` in your workspace, and push them to the bare repository `origin master`.
Wait at least 5 seconds after pushing to allow the hook to execute, the C program to compile, and the supervisor to run and restart at least once. 

Once you have pushed the code and verified that `/home/user/processed.log` contains the expected output (including the `RESTARTING PARSER` message and the Tokyo timezone dates), you are done.