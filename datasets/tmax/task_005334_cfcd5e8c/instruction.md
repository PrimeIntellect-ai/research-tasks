You are a deployment engineer tasked with rolling out a new filesystem backup update. We are transitioning our log backup system to a new Rust-based agent that must securely tunnel its traffic.

The configuration for this deployment was handed off as an architecture diagram image located at `/app/deployment_spec.png`. 

Your objectives are:
1. **Extract Configuration:** Analyze `/app/deployment_spec.png` (using `tesseract` or similar tools) to find the assigned `BACKUP_SERVER_PORT` and `LOCAL_TUNNEL_PORT`.
2. **Establish Secure Tunnel:** The target backup server is currently running locally on the `BACKUP_SERVER_PORT`. You must establish a background SSH tunnel that forwards local connections from the `LOCAL_TUNNEL_PORT` to the `BACKUP_SERVER_PORT` on `localhost`. The `user` account already has SSH keys configured for passwordless access to `localhost`.
3. **Write the Backup Agent:** In `/home/user/backup_agent`, initialize a Rust binary project. Write a Rust program that:
   - Reads all files in the `/home/user/telemetry_data/` directory.
   - Compresses the contents of the directory into a single GZIP stream (tar.gz format is recommended but a plain gzipped concatenation or similar is fine, as long as it compresses well). 
   - Connects to `localhost` on the `LOCAL_TUNNEL_PORT` via TCP.
   - Transmits the compressed byte stream over the TCP connection and gracefully closes the connection.
   - **Optimization Requirement:** The raw telemetry data is highly redundant. Your Rust compression implementation must be efficient. The final transferred payload must be smaller than 50,000 bytes.
   - Build the program in release mode.
4. **Schedule the Agent:** Configure a cron job for the `user` account to run the compiled Rust binary every minute.

To test your deployment, you can manually trigger your Rust binary. A mock backup listener is already running on the `BACKUP_SERVER_PORT` and will save the first connection's payload to `/home/user/received_backup.dat`.

You are finished when the SSH tunnel is active, the cron job is installed, and the final compressed payload has been successfully received at `/home/user/received_backup.dat`.