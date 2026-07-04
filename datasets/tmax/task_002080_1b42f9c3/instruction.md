You are a network engineer troubleshooting connectivity issues. An internal proxy is returning 502 Bad Gateway errors because our custom socket path resolver is outputting the wrong Unix domain socket paths.

We use a custom tool written in Rust to parse internal URIs and map them to filesystem socket paths. The source code for this tool is vendored at `/app/socket_resolver`. Recently, a bad commit broke its parsing logic. 

Your tasks are:
1. **Fix the Rust Package:**
   Analyze and fix the Rust project in `/app/socket_resolver`. The tool reads a single URI string from standard input and prints the socket path to standard output. 
   The exact specification it must follow is:
   - Input format: `upstream://<host>:<port>/<path>`
   - Outputs: `/home/user/run/upstream/<host>_<port>_<path>.sock`
   - Constraints: `<host>`, `<port>`, and `<path>` will consist only of alphanumeric characters. 
   - If the input does NOT strictly match the prefix `upstream://` or is missing the host, port, or path components separated by `:` and `/` exactly as specified, the tool must output exactly the string `INVALID`.
   - Ensure the output has no trailing newline character (or standard trailing newline is fine, but be consistent with basic `print!` or `println!` - the automated fuzzer expects a newline at the end). Wait, the fuzzer expects standard `println!`.
   - Build the release binary. The compiled binary must be located at `/app/socket_resolver/target/release/socket_resolver`.

2. **Backup Configuration:**
   We have a supervisord configuration file at `/home/user/supervisor/conf.d/resolver.conf`. Create a backup of this file at `/home/user/backups/resolver.conf.bak`.

3. **Process Supervision:**
   Update the supervisord configuration at `/home/user/supervisor/conf.d/resolver.conf` to supervise the newly built binary. The service name must remain `resolver_daemon`. It should execute `/home/user/wrapper.sh` (which wraps your binary). Ensure the service is set to auto-restart on failure.

4. **Log Rotation:**
   The wrapper script writes logs to `/home/user/logs/resolver.log`. Create a logrotate configuration file at `/home/user/logrotate.d/resolver` that rotates this specific log file daily, keeps 7 backups, and compresses old logs.

Do not use root/sudo privileges, everything should be done as the `user` user in their home directory or `/app`.