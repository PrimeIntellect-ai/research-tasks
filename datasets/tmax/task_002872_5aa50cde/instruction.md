You are an incident responder investigating a potential compromise on a Linux workstation. 

We have isolated a suspicious compiled executable located at `/home/user/suspicious_beacon`. Our initial analysis indicates that when executed, this binary silently binds to a local port (between 10000 and 40000) on `127.0.0.1` and listens for incoming connections. Furthermore, we suspect the beacon requires a specific authentication token to accept commands. 

Your objective is to analyze this binary and generate the correct access token. 

Complete the following steps:
1. Start the `/home/user/suspicious_beacon` binary in the background.
2. Use standard service auditing tools to determine the exact TCP port it is listening on.
3. Perform static analysis / reverse engineering on the binary to locate a hardcoded authentication salt. The salt is a distinct string starting with the prefix `B34C0N_S4LT_`.
4. Generate the valid authentication token. The token algorithm is known to be the SHA-256 hash (in standard lowercase hex format) of the exact string concatenation of the salt and the port number (i.e., `<salt><port_number>`). Ensure there are no trailing newlines in the input string before hashing.
5. Record your findings in a report file at `/home/user/report.txt`.

The `/home/user/report.txt` file must contain exactly three lines in the following format:
```
PORT=<discovered_port>
SALT=<discovered_salt>
TOKEN=<computed_sha256_token>
```

Ensure the binary is running, and you only use standard shell utilities and scripts to accomplish this.