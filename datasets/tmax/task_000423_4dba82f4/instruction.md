You are acting as a Site Reliability Engineer responsible for monitoring network uptime. We have a locally vendored copy of `fping` that we need to use for our custom internal monitoring pipeline, but the build process is currently broken. 

Your task consists of two parts:

Part 1: Fix and Build `fping`
The source code for `fping` version 5.1 is vendored at `/app/fping-5.1`. 
1. The `configure` script lacks executable permissions.
2. There is a deliberate syntax error injected into `src/Makefile.am` (an invalid variable assignment `CC_BROKEN = 1` that breaks the build toolchain generation).
Fix these issues, generate the build files (you may need to run `autoreconf -i`), run `./configure`, and compile the software using `make`. You do not need to install it globally; leaving the compiled binary at `/app/fping-5.1/src/fping` is sufficient.

Part 2: Create the Uptime Parser
We need a robust parser that processes raw, interactive-like ping logs (which sometimes contain ANSI escape codes, interactive prompts, and network errors) and outputs a clean CSV format.
Write a script at `/home/user/uptime_parser.sh` (or any other executable file, e.g., `/home/user/uptime_parser.py`, as long as it is an executable script at `/home/user/uptime_parser`).

The script must:
1. Read lines from standard input (stdin). 
2. Filter out any lines containing the exact string `interactive-prompt>`.
3. Extract the IP address and the packet loss percentage from `fping` summary lines. A standard `fping` summary line looks like: `192.168.1.1 : xmt/rcv/%loss = 10/8/20%`
4. Print the extracted data to standard output (stdout) in strict CSV format: `IP,Loss` (without a header). For the example above, it must output exactly `192.168.1.1,20`.
5. Ignore any lines that do not match the `xmt/rcv/%loss` pattern.
6. Strip any leading or trailing whitespace from the output lines.

Ensure your script is executable (`chmod +x /home/user/uptime_parser`). Your script will be tested via a fuzzing engine that streams thousands of randomly generated `fping` outputs to ensure it perfectly matches our reference implementation.