You are an incident responder investigating a suspicious data processing worker deployed on a compromised Linux host. The attackers left behind the binary and its systemd service configuration in `/home/user/investigation/`. 

Your goal is to analyze the binary without executing it on the host, identify how it was achieving privilege escalation, and construct a sandbox to safely run it.

Perform the following tasks:

1. **Privilege Escalation Auditing:**
   Audit the file `/home/user/investigation/worker.service`. The attackers modified this service to execute arbitrary commands with elevated privileges during the service startup process, bypassing normal restrictions. Identify the exact line in this file that implements this privilege escalation (hint: look for misconfigured execution directives). Write the exact, full line (exactly as it appears in the service file, preserving whitespace) into `/home/user/priv_escalation.txt`.

2. **Binary Format and ELF Analysis:**
   The suspicious binary is located at `/home/user/investigation/data_worker`. We suspect the attackers hid their command-and-control IP address inside a custom ELF section called `.mal_cfg`.
   Write a Python script at `/home/user/extract_config.py` that reads the raw bytes of the `.mal_cfg` section from the ELF binary and writes the decoded ASCII string to `/home/user/extracted_config.txt`. You may use the `pyelftools` library (`pip install pyelftools`). Do not execute the `data_worker` binary.

3. **Process Isolation and Sandboxing:**
   We need to safely observe the binary's data processing behavior. The binary reads from `/tmp/input.dat` and writes to `/tmp/output.dat`. 
   Write a bash script at `/home/user/safe_run.sh` that uses `bwrap` (Bubblewrap) to execute `/home/user/investigation/data_worker`. 
   The sandbox must enforce the following strict isolation:
   - Mount a new, empty `tmpfs` on `/tmp` (do NOT bind the host's `/tmp`).
   - Bind mount the host's `/usr` and `/lib` (and `/lib64` if it exists) directories as strictly read-only so the binary can load shared libraries.
   - Bind mount `/home/user/investigation` as strictly read-only.
   - Run the binary `/home/user/investigation/data_worker` inside the sandbox.
   - Drop all capabilities and unshare all namespaces (user, pid, ipc, net, uts).

Ensure `/home/user/safe_run.sh` is executable. You do not need to run the bash script yourself, but it must be valid for our automated testing system to execute.