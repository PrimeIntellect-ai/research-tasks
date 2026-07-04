You are a network security engineer tasked with securing an authentication service and implementing a rudimentary intrusion detection mechanism. 

Currently, a legacy authentication wrapper script `/home/user/run_auth.sh` invokes a Python script `/home/user/auth_service.py` to validate user credentials. The system has three critical security issues that you must resolve:

**Phase 1: Fix Process Credential Leak**
The current `run_auth.sh` script takes a username and password as arguments and passes them directly to `auth_service.py` via command-line arguments (e.g., `python3 /home/user/auth_service.py --user <user> --password <pass>`). This is a massive security risk because the password becomes temporarily visible to all users on the system via `/proc/[pid]/cmdline` or the `ps` command.
1. Modify `/home/user/run_auth.sh` to pass the password to the Python script using an environment variable named `AUTH_SECRET` instead of a command-line argument. The script still receives the username as `$1` and password as `$2`.
2. Modify `/home/user/auth_service.py` to read the password from the `AUTH_SECRET` environment variable. Ensure it still accepts the `--user` argument. 

**Phase 2: Intrusion Detection (Pattern Matching)**
You have been provided a simulated traffic log file at `/home/user/traffic.log`. Each line is a JSON object representing an authentication attempt, with keys: `timestamp`, `ip`, `user`, and `status` ("success" or "failed").
1. Write a Python script at `/home/user/ids_monitor.py` that reads `/home/user/traffic.log`.
2. The script must identify any `ip` address that has **3 or more consecutive failed authentication attempts** against the *same* `user` account. A successful login resets the consecutive failure counter for that IP/user combination.
3. Your script must write the offending IP addresses (one per line, sorted in ascending alphabetical/lexicographical order) to `/home/user/flagged_ips.txt`.

**Phase 3: Process Isolation (Sandboxing)**
To prevent future vulnerabilities in `auth_service.py` from compromising the host, the service should be run inside a sandbox. 
1. Construct a Bubblewrap (`bwrap`) command that executes `/home/user/auth_service.py --user guest` in a sandbox.
2. The sandbox must meet these exact requirements:
   - Bind the root filesystem `/` as read-only (`--ro-bind`).
   - Mount a new procfs at `/proc` (`--proc /proc`).
   - Mount a new devfs at `/dev` (`--dev /dev`).
   - Create a temporary filesystem at `/tmp` (`--tmpfs /tmp`).
   - Isolate all namespaces including network (`--unshare-all`).
3. Save the exact `bwrap` command string as a single line in the file `/home/user/sandbox_cmd.txt`. (Do not execute it, just write the command to the file).

Complete all phases to secure the authentication pipeline.