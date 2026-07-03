You are a Site Reliability Engineer (SRE) tasked with deploying a new Rust-based uptime monitoring service. Our internal services are isolated, so the monitor needs to connect via an SSH tunnel. You must write the Rust monitor, create a robust staged deployment script, and verify that the alerting system works when the service goes down.

Here are your instructions:

1. **Setup the SSH Tunnel**
   There is a dummy health-check service running on port `9090`.
   Establish a local background SSH tunnel that forwards local port `8080` to local port `9090`. Connect to `localhost` as your current user (`user`). (Your SSH keys are already configured for passwordless login to localhost). 

2. **Develop the Rust Monitor**
   In the directory `/home/user/monitor_src/`, there is an initialized Cargo project with `reqwest`, `tokio`, and `lettre` dependencies already in the `Cargo.toml`. 
   Write the application logic in `/home/user/monitor_src/src/main.rs`. The program must:
   - Perform an asynchronous HTTP GET request to `http://localhost:8080/health`.
   - Implement error handling: if the request succeeds with a 200 OK status, print "Service is UP" to stdout.
   - If the request fails (e.g., connection refused, timeout, or non-200 status), the monitor must generate an email alert.
   - Instead of sending over SMTP, configure `lettre` to use a `FileTransport` writing to the directory `/home/user/mail_spool/`.
   - The generated email must have the exact Subject: `ALERT: Service Down`, From: `sre@localhost`, and To: `admin@localhost`. The body can contain the error details.

3. **Write a Staged Deployment Script**
   Write a robust bash script at `/home/user/deploy.sh` that performs a staged deployment of your Rust monitor. The script must:
   - Compile the Rust project in `/home/user/monitor_src/` using `cargo build --release`.
   - Copy the compiled binary to the staging area: `/home/user/deploy/staging/monitor`.
   - Verify the binary is executable.
   - If successful, promote it by copying it to the production area: `/home/user/deploy/production/monitor`.
   - Handle errors gracefully (e.g., `set -e`, echo error messages).
   - Append the line `Deployment successful` to `/home/user/deployment.log` if all steps pass.

4. **Execute and Trigger the Alert**
   - Run your `deploy.sh` script to deploy the monitor.
   - Run the production binary `/home/user/deploy/production/monitor` to verify it prints "Service is UP" (since the SSH tunnel is active).
   - Kill the SSH tunnel (or the background SSH process) you created in step 1.
   - Run the production binary `/home/user/deploy/production/monitor` again. Because the tunnel is down, the request should fail, and your Rust code should write an `.eml` alert file into `/home/user/mail_spool/`.

Complete these steps using the terminal. Ensure all file paths and required strings exactly match the instructions.