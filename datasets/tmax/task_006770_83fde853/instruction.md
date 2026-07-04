You are a Linux Systems Engineer tasked with hardening network configurations for a simulated local micro-service environment. 

We have a custom C utility, `/home/user/net_parser.c`, designed to read custom port-forwarding and firewall rules from a text file. Currently, the environment is misconfigured—services can't reach each other because `net_parser.c` crashes when it encounters malformed inputs, and it produces inconsistent timestamps due to missing timezone/locale enforcement in the environment.

Your task consists of two parts:

1. **Debug and Fix `/home/user/net_parser.c`**
   The source code in `/home/user/net_parser.c` reads lines from a file path provided as its first argument. It expects lines in the format: `ACTION PORT1 PORT2` (e.g., `FORWARD 8080 80` or `DROP 22 -1`). 
   - Fix the program so it robustly handles malformed lines (e.g., lines with missing ports, or non-integer values) by silently skipping them instead of crashing, infinite looping, or producing garbage values. 
   - Ensure the program compiles cleanly with `gcc` without warnings.
   - The output of the C program for valid lines should remain: `[VALID] <ACTION> <PORT1> <PORT2>`

2. **Create the automation script `/home/user/run_audit.sh`**
   Write a robust bash script at `/home/user/run_audit.sh` that does the following:
   - Temporarily sets the environment timezone to `UTC` and the locale to standard `C` (`LC_ALL=C`) for the duration of the script execution.
   - Compiles `/home/user/net_parser.c` into an executable named `/home/user/net_parser`.
   - Executes `/home/user/net_parser` against the configuration file `/home/user/rules.txt`.
   - Uses a text processing pipeline (`awk`, `sed`, or `grep`) to format the valid output lines. The final formatted text must be saved to `/home/user/audit_report.log`.
   - The formatting requirement for `/home/user/audit_report.log` is:
     For a valid line output by the C program `[VALID] FORWARD 8080 80`, the script must append to the log: `Audit - Action: FORWARD, Mapping: 8080->80`. 
     If the action is `DROP` (e.g., `[VALID] DROP 22 -1`), it should be: `Audit - Action: DROP, Mapping: 22`.

Make sure `/home/user/run_audit.sh` is executable (`chmod +x`). All tasks must be completed in `/home/user`.