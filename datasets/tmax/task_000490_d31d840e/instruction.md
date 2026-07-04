We have a custom network health-check service that is failing to start up properly. The service relies on a proprietary compiled binary located at `/app/net_health_checker`. Unfortunately, the source code was lost, and the binary is stripped. 

We need to replace this binary with a Python script to restore the service and allow us to maintain it in the future. 

Your task is to:
1. Analyze the `/app/net_health_checker` binary to understand its behavior. It takes a single command-line argument: the path to a log file. 
2. The log file contains network connection attempts in a specific proprietary format. The binary parses this file, performs some basic connectivity diagnostics based on the parsed data, and outputs a very specific health status report to stdout.
3. Write a Python script at `/home/user/net_health_checker.py` that replicates the EXACT behavior and output of the original binary for any valid or invalid input log file. Your script must be bit-exact equivalent in its standard output and exit codes.
4. Configure a log rotation policy for `/var/log/net_health.log` (assume you have write access to the log directory and the logrotate config directory at `/home/user/logrotate.d/`) to rotate daily, keep 7 days of logs, compress them, and create a new log file with permissions `0644`. Save the logrotate configuration at `/home/user/logrotate.d/net_health`.

Ensure your Python script is executable and processes the log file path provided as its first argument.