You are a container specialist testing a new sidecar pattern for a microservice environment. You need to implement a dummy C microservice, secure it with TLS, expose it through an SSH tunnel to simulate cross-container traffic, and create a monitoring daemon.

Complete the following tasks in the `/home/user` directory:

1. **C Microservice**
Write a C program at `/home/user/auth_svc.c` that, when executed, prints the following HTTP response to standard output (ensure you include the exact CRLF newlines for HTTP headers, followed by the JSON payload on a single line with a trailing newline):
```text
HTTP/1.1 200 OK
Content-Type: application/json

{"status":"healthy","service":"auth-service"}
```
Compile the program to the executable `/home/user/auth_svc`.

2. **TLS Server Setup**
Generate a self-signed RSA 2048-bit certificate and private key. Save them as `/home/user/server.crt` and `/home/user/server.key` respectively (skip any interactive prompts by providing default subjects). 
Use `socat` to create a TLS listener on port `8443` that executes `/home/user/auth_svc` for each incoming connection. Combine the key and certificate into a `.pem` file if required by `socat`. Run this listener in the background.

3. **SSH Tunneling**
Generate an ed25519 SSH keypair without a passphrase at `/home/user/.ssh/id_ed25519`. Authorize this key for the current user so you can SSH into `localhost` without a password.
Create an SSH tunnel in the background that binds local port `9090` and forwards it to `localhost:8443`. (Use `StrictHostKeyChecking=no` to bypass prompt issues).

4. **Monitoring Daemon**
Create a bash script at `/home/user/monitor.sh` that acts as a custom scheduler. The script should run an infinite loop that does the following every 2 seconds:
- Sends a GET request to `https://localhost:9090` (ignoring TLS certificate warnings).
- Extracts *only* the JSON body from the response.
- Appends the extracted JSON line to `/home/user/health_log.txt`.
Start this script in the background. Wait at least 6 seconds to ensure `health_log.txt` accumulates at least 3 lines of logs before completing your turn.