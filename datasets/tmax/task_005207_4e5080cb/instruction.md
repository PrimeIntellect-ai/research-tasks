You are tasked with fixing a startup race condition and creating a monitoring pipeline for a pair of user-space services. 

Currently, there is a startup script located at `/home/user/services/start_services.sh`. It starts two Python services: `producer.py` and `consumer.py`. However, `consumer.py` crashes because it requires `producer.py` to be fully initialized and listening on port `8080` before it starts, but the current script starts them simultaneously.

Perform the following tasks to harden this configuration:

1. **Create a Health Check Script:**
   Write a Python script at `/home/user/services/health_check.py` that accepts a host and a port as command-line arguments (e.g., `python3 health_check.py 127.0.0.1 8080`). 
   - The script should continuously attempt to establish a TCP connection to the specified host and port.
   - It should retry every 1 second.
   - If it successfully connects, it should close the connection and immediately exit with status code `0`.
   - If it fails to connect within 15 seconds, it should exit with status code `1`.

2. **Fix the Service Lifecycle script:**
   Modify `/home/user/services/start_services.sh` to correctly sequence the services:
   - Start `python3 /home/user/services/producer.py` in the background.
   - Use your `health_check.py` script to wait for `127.0.0.1` port `8080` to become available.
   - Only after the health check exits successfully (`0`), start `python3 /home/user/services/consumer.py` in the background.
   - The script must write the PIDs of both `producer.py` and `consumer.py` (each on a new line) to `/home/user/services/run.pid`.

3. **Log Monitoring Pipeline:**
   `producer.py` outputs its logs to `/home/user/services/app.log`. Once the services are successfully running and communicating, `producer.py` will log several messages, including some critical error simulations.
   Create a bash script at `/home/user/services/log_monitor.sh` that processes `/home/user/services/app.log`. 
   - Using standard bash text processing tools (awk, grep, sed, etc.), find all lines containing the string `CRITICAL`.
   - The log lines are space-separated. Extract *only* the 5th column (which represents the error code) from these lines.
   - Save these extracted error codes, one per line, into `/home/user/services/critical_codes.txt`.

Run your fixed `start_services.sh` script, wait for about 10 seconds to let the consumer generate traffic, and then run your `log_monitor.sh` script to generate the final output file.