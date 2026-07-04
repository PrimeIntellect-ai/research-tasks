You are a capacity planner analyzing resource usage across simulated infrastructure. We have a multi-service setup located in `/app/` that needs to be deployed and reconfigured to correctly process metrics.

Currently, there are two components:
1. `/app/collector.cpp` - A C++ daemon that receives metrics over TCP. 
2. `/app/logger.sh` - A bash script that aggregates and rotates logs.

Due to a configuration mismatch (similar to an SSH config silently rejecting key-based logins), the collector drops incoming metrics without properly delegating them to the logger.

Your task is to:
1. Compile the C++ collector to an executable named `/home/user/bin/collector`.
2. Analyze the `collector.cpp` source to find which local port it uses to communicate with the logging service, and update `/app/logger.sh` to listen on that exact port (it's currently misconfigured).
3. Set up the environment by executing `/app/logger.sh` and `/home/user/bin/collector` in the background. 
4. The collector daemon must run inside a basic user namespace to simulate our container lifecycle process. Launch it using: `unshare -U -r /home/user/bin/collector`.
5. Create a `logrotate` configuration file at `/home/user/config/logrotate.conf` that rotates the logger's output file `/home/user/logs/capacity.log` daily, keeping 3 backups.

When correctly configured, the C++ collector should listen on TCP port `8888` on `127.0.0.1`. When it receives the string `CAPACITY_REPORT <value>\n`, it should forward it to the logger and respond back to the TCP client with `OK_RECORDED\n`.

Make sure both services are running in the background and listening on their respective ports when you finish.