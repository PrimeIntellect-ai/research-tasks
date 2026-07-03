You are a system administrator tasked with building a lightweight, secure deployment manager in Python. This tool will simulate container lifecycle management by starting and stopping an isolated, TLS-secured web server process.

Your objective is to perform the following steps exclusively via the command line:

1. Create a base directory `/home/user/deploy_system`.
2. Inside it, create a directory called `public`.
3. Create a file `/home/user/deploy_system/public/payload.json` containing exactly: `{"status": "securely deployed"}`
4. Write a Python script at `/home/user/deploy_system/manager.py`. This script must handle two commands via CLI arguments: `start` and `stop` (e.g., `python3 manager.py start`).
   
   When invoked with `start`, the script must:
   - Check for the existence of `/home/user/deploy_system/cert.pem` and `/home/user/deploy_system/key.pem`. If they do not exist, use `subprocess` to generate a self-signed RSA-2048 certificate (valid for 365 days, no passphrase, Subject CN=localhost) using `openssl`.
   - Start a Python HTTPS server (using standard library modules like `http.server` and `ssl`) on port `9443` serving the `/home/user/deploy_system/public` directory.
   - Run the server process in the background.
   - Write the process ID (PID) of the server to `/home/user/deploy_system/app.pid`.
   - Log all standard output and standard error from the server to `/home/user/deploy_system/app.log`.

   When invoked with `stop`, the script must:
   - Read the PID from `/home/user/deploy_system/app.pid`.
   - Terminate the process cleanly.
   - Delete the `/home/user/deploy_system/app.pid` file.

5. After constructing `manager.py`, execute the following lifecycle steps using your script:
   - Start the server using your script.
   - Wait 2 seconds for the server to initialize.
   - Use `curl` to fetch the payload securely (ignoring cert warnings) via `https://localhost:9443/payload.json` and save the exact output to `/home/user/deploy_system/test_result.txt`.
   - Stop the server using your script.

Ensure all paths are absolute and correct. Make sure your Python script runs robustly using the standard library.