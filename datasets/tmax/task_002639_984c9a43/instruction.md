You are a monitoring specialist tasked with fixing a local logging and alerting pipeline for a mock microservice architecture. 

Currently, there is a local service orchestration script located at `/home/user/app/start_services.sh`. It is supposed to spin up three simulated "container" processes:
1. A log generator (`generator.sh`)
2. A metrics aggregator (`aggregator.sh`)
3. An alert sink (`sink.sh`)

However, the services are failing to communicate. They rely on a shared filesystem mount point and specific environment variables to function, but the configuration is currently broken.

Your tasks are:
1. **Fix the Service Configuration:**
   Inspect and fix the environment variables and shared directory paths in `/home/user/app/config.env` and `/home/user/app/start_services.sh`. The generator must write its logs to `/home/user/app/shared_logs/`, which needs to be virtually "mounted" (symlinked or directly configured in the env vars) so the aggregator and sink can read from the exact same location. Ensure all three processes start and stay running. Create any missing directories with standard user permissions.

2. **Implement the Binary Log Parser in C:**
   The logs generated in the shared directory are in a custom binary format. You must write a C program at `/home/user/workspace/alert_parser.c` that reads these binary logs from `stdin` and prints formatted text to `stdout`.
   We have provided a compiled reference binary (oracle) at `/home/user/app/oracle_parser`. Your C program must produce **bit-exact identical output** to this oracle for any valid or invalid binary input. 
   
   *Reverse Engineering the Format:* You can pass random bytes or sample logs from `/home/user/app/shared_logs/` into `/home/user/app/oracle_parser` to deduce the parsing logic. (Hint: It reads 8-byte chunks consisting of a 4-byte timestamp, a 2-byte alert ID, and a 2-byte severity level, all little-endian. It prints "ALERT: [ID] at [timestamp] with severity [severity]\n". Invalid sized chunks at EOF should be ignored.)
   
   Compile your program to `/home/user/workspace/alert_parser`.

3. **Process Monitoring:**
   Write a bash script at `/home/user/workspace/monitor.sh` that continuously runs your `alert_parser` program, feeding it data from `/home/user/app/shared_logs/generator.bin` via `tail -f`, and piping the output to `/home/user/workspace/alerts.log`. If your parser crashes or exits, the monitor script must restart it within 1 second. Set up your shell profile (`/home/user/.bashrc`) to export a variable `MONITOR_ACTIVE=1`.

Verify your setup by ensuring `/home/user/workspace/alerts.log` is continuously populated with the parsed text. Do not modify the oracle binary.