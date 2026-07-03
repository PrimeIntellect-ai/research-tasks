You are a Linux Systems Engineer tasked with hardening the configuration and execution flow of a custom CI/CD runner. You need to implement a lightweight Go-based authorization wrapper that performs user group administration checks and connectivity diagnostics before allowing a pipeline step to execute. 

Everything should be created inside the `/home/user/ci-runner` directory.

Perform the following steps:

1. Create a Role-Based Access Control (RBAC) configuration file named `/home/user/ci-runner/roles.conf`.
The file must contain exactly these user-to-group-to-command mappings (one per line, format `username:group:allowed_commands_comma_separated`):
```
alice:dev:deploy,status
bob:admin:deploy,status,restart
charlie:qa:status
```

2. Write a Go program at `/home/user/ci-runner/main.go` that acts as the CI/CD runner authorization wrapper. 
The program must:
- Accept exactly 3 positional arguments (after the program name): `user`, `cmd`, and `endpoint`. (Example: `./runner bob restart localhost:8080`)
- Step A (Connectivity Diagnostic): Attempt to establish a TCP connection to the provided `endpoint`. If the connection fails (e.g., connection refused or timeout), print `ENDPOINT_UNREACHABLE` to standard output and exit with status code `2`.
- Step B (User Admin Check): If the endpoint is reachable, read `/home/user/ci-runner/roles.conf`. Check if the given `user` is allowed to execute the given `cmd` based on their allowed commands in the file.
- If the user does not exist or is not authorized for the command, print `ACCESS_DENIED` to standard output and exit with status code `3`.
- If the user is authorized, print `ACCESS_GRANTED` to standard output and exit with status code `0`.

3. Write a bash script `/home/user/ci-runner/pipeline.sh` that automates the building and testing of this runner. The script must:
- Create the `bin` directory (`/home/user/ci-runner/bin`).
- Compile `main.go` into an executable named `/home/user/ci-runner/bin/runner`.
- Start a background process listening on TCP port `8080` on `localhost` (using `nc -l 8080` or similar shell tools) to simulate a healthy pipeline endpoint. Ensure it is ready to accept connections.
- Execute the compiled runner with arguments: user `bob`, command `restart`, and endpoint `localhost:8080`.
- Redirect the standard output of the runner to `/home/user/ci-runner/test.log`.
- Terminate the background listener process cleanly.

Ensure your `pipeline.sh` is executable (`chmod +x`). Once you have written everything, execute `/home/user/ci-runner/pipeline.sh` to generate the `test.log` file.