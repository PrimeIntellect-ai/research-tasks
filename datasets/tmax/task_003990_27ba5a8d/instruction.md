You are a system administrator tasked with auditing server configurations and automating an interactive legacy service via local port forwarding.

Because you do not have root access on this system, you will be working with a copy of system files and simulating the network setup locally. 

Please perform the following tasks:

1. **User Account Administration Audit**:
   You have been provided with mock configuration files at `/home/user/sysfiles/passwd` and `/home/user/sysfiles/group`.
   Find all usernames that are members of the `admin` group. A user is considered a member if:
   - Their primary Group ID (GID) in the `passwd` file matches the GID of the `admin` group in the `group` file.
   - OR they are listed as a supplementary member in the `admin` group entry in the `group` file.
   Write the list of these usernames to `/home/user/admin_users.txt`, with one username per line, sorted alphabetically. You may write a Python script to compute this.

2. **Port Forwarding**:
   There is a legacy interactive Python service located at `/home/user/legacy_service.py` that will listen on `127.0.0.1:8888` when executed. 
   Write a Python script at `/home/user/port_forward.py` that acts as a simple TCP proxy. It must listen on `127.0.0.1:9999` and forward all bidirectional traffic to `127.0.0.1:8888`. It should be able to handle at least one connection at a time. Do not use external libraries; use Python's built-in `socket` module.

3. **Expect Scripting**:
   Write an Expect script at `/home/user/automate.exp` that automates logging into this legacy service through your port forwarder. 
   The script must:
   - Spawn a connection using `nc 127.0.0.1 9999`.
   - Wait for the exact string: `Username: `
   - Send the string: `admin` followed by a newline.
   - Wait for the exact string: `Password: `
   - Send the string: `supersecret` followed by a newline.
   - Wait for the exact string: `Access Granted`
   - Exit with a status of `0` upon success.

Make sure the Expect script is executable (`chmod +x /home/user/automate.exp`).