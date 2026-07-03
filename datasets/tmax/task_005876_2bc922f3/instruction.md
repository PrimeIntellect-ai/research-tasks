You are acting as a network engineer building an interactive, role-based connectivity diagnostic tool. Because you do not have root access on this system, you must implement a custom role-based access control (RBAC) system for this tool rather than using system-level user groups.

Your task is to create a Go-based diagnostic application and an accompanying shell setup script. All work must be contained within `/home/user/network_diag/`.

Step 1: Write a shell script `/home/user/network_diag/setup.sh`
This script must perform the following actions:
1. Create the directory `/home/user/network_diag/` if it doesn't exist.
2. Generate a JSON configuration file at `/home/user/network_diag/roles.json` with exactly the following content:
```json
{
  "netadmin": ["127.0.0.1:9001", "127.0.0.1:9002", "127.0.0.1:9003"],
  "appdev": ["127.0.0.1:9001"],
  "guest": ["127.0.0.1:9003"]
}
```
3. Compile a Go program (which you will write in Step 2) named `/home/user/network_diag/diag.go` into an executable named `/home/user/network_diag/diag_tool`.

Step 2: Write the Go program `/home/user/network_diag/diag.go`
This program must be an interactive command-line tool that does the following:
1. Prompts the user on standard output exactly with: `Enter username: `
2. Reads a single string from standard input.
3. Loads `/home/user/network_diag/roles.json`. If the entered username is not a key in this JSON, print `Access Denied` to standard output and exit with status code 1.
4. If the user exists, iterate over the list of endpoints associated with that user.
5. For each endpoint, attempt a TCP connection using Go's `net.DialTimeout` with a timeout of exactly 1 second.
6. For each endpoint, append a result line to `/home/user/network_diag/audit.log`. The file should be created if it does not exist.
7. The format of the line in `audit.log` must be EXACTLY:
   `[USERNAME] checked [ENDPOINT]: [STATUS]`
   Where `[STATUS]` is either `OK` (if the TCP connection succeeded) or `FAIL` (if it timed out or was refused).
   Example: `[netadmin] checked 127.0.0.1:9001: OK`

Step 3: Verification Preparation
Before you finish, ensure that you run your `setup.sh` script to build the tool and create the configuration files. You do not need to start any background services or run the `diag_tool` yourself; the automated test suite will start local listeners on ports 9001 and 9002 (leaving 9003 closed) and will interactively pipe usernames into your compiled binary to verify the `audit.log` output.