You are a cloud architect migrating a legacy custom logging and routing analytics service. We rely on a vendored package located at `/app/log-router-v1.2` which parses incoming SSH connection logs, extracts locale and timezone data from the payload, and outputs a formatted routing directive string for our network interface configurations. 

However, during the migration, we discovered that the vendored package has a bug: it silently drops log entries that contain a specific SSH key rejection pattern (`"Disconnecting: Too many authentication failures"`), causing our log rotation scripts to miss vital security events. Furthermore, the routing configuration module miscalculates the UTC offsets when the locale is set to `fr_FR.UTF-8`.

Your task is to:
1. Fix the source code of the vendored package in `/app/log-router-v1.2/src/parser.py` (which interfaces with a C-extension for speed) so that it correctly parses and formats the SSH rejection logs and calculates the correct UTC offset for the `fr_FR.UTF-8` locale.
2. Ensure the system has the `fr_FR.UTF-8` locale installed and generated.
3. Configure a log rotation rule in `/home/user/logrotate.conf` that rotates the output files in `/home/user/logs/` daily, keeping 7 days of logs.
4. Provide a wrapper script at `/home/user/process_logs.sh` that takes a log file as an argument and outputs the parsed routing directives to stdout.

Your final wrapper script `/home/user/process_logs.sh` must behave EXACTLY like our reference binary (which handles the edge cases perfectly) for any given input log.