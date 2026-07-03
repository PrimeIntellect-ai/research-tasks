You are a Site Reliability Engineer (SRE) investigating an issue with our internal uptime tracking service. The service is a small C++ application that reads simulated container health logs, calculates the overall uptime percentage, and reports it. 

We are currently facing two issues:
1. **Environment Misconfiguration / Missing Logs**: The monitoring script `run_monitor.sh` is failing to find the container logs. You'll need to locate the correct directory where the actual container logs are being stored in the filesystem (they should be somewhere in `/home/user/container_logs/`) and fix the environment variable in `/home/user/run_monitor.sh` so the C++ program reads from the correct log file (`health.log`).
2. **Precision Loss**: Even when pointed to the correct file, the C++ program calculates the uptime incorrectly as `0.0000%`. There is a precision loss issue in `/home/user/uptime_monitor.cpp` where the uptime percentage calculation truncates the result before formatting it.

Your tasks:
1. Fix the environment variable exported in `/home/user/run_monitor.sh` to point to the correct log directory containing `health.log`.
2. Fix the precision loss bug in `/home/user/uptime_monitor.cpp` so that the percentage evaluates correctly (it should evaluate to `99.9950%` based on the log data, not `0.0000%`).
3. Recompile the C++ program using `g++ /home/user/uptime_monitor.cpp -o /home/user/uptime_monitor`.
4. Run the fixed `/home/user/run_monitor.sh` script and redirect its output to `/home/user/final_uptime.txt`.

The final `/home/user/final_uptime.txt` should contain exactly:
`System Uptime: 99.9950%`