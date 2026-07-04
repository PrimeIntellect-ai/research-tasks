You are a Site Reliability Engineer (SRE) investigating an issue with a custom uptime monitoring daemon. The daemon is located in a local Git repository at `/home/user/uptime_monitor`. 

Recently, the monitor stopped reporting uptime. You've identified two separate issues that need to be resolved:

1. **Missing Authentication:** The monitor requires an authentication token passed as a command-line argument. The token was accidentally deleted from the repository in a recent commit. You need to perform forensics on the Git history of `/home/user/uptime_monitor` to find the lost token.
   - Once found, write the exact token value (just the string itself, no extra text) to `/home/user/recovered_token.txt`.

2. **Daemon Hang (Infinite Loop):** Even if you have the token, running the monitor currently causes it to hang indefinitely. There is an algorithmic bug in `monitor.c` related to numerical precision that prevents a critical loop from terminating.
   - Use debugging tools (e.g., `strace` or `gdb`) or code inspection to identify why the loop never finishes.
   - Modify `monitor.c` to fix the loop termination and precision issue so that the program successfully finishes executing. 
   - Recompile the program by running `make` in the `/home/user/uptime_monitor` directory.

After successfully recovering the token and fixing the C code, run the monitor daemon using the recovered token and redirect its standard output to a log file:
```bash
cd /home/user/uptime_monitor
./monitor $(cat /home/user/recovered_token.txt) > /home/user/monitor_output.txt
```

Your task is considered complete when both `/home/user/recovered_token.txt` and `/home/user/monitor_output.txt` exist and contain the correct values.