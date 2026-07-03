You are an administrator for a small site, managing user storage. You need to create a custom monitoring tool in Rust that checks a user's disk usage, tests connectivity to a remote metrics server, and optionally provides an SSH tunneling command if the server is unreachable.

Write a Rust program at `/home/user/quota_monitor.rs` and compile it to `/home/user/quota_monitor`. 

The program must do the following when executed with no arguments:
1. Calculate the total size in bytes of all files in the directory `/home/user/user_data` (recursive).
2. If the total size exceeds 5,000 bytes, the program must attempt to open a TCP connection to `127.0.0.1:5555` (our local metrics endpoint).
3. If the connection is successful, send the string `QUOTA_EXCEEDED:<TOTAL_BYTES>` (e.g., `QUOTA_EXCEEDED:5120`) to the TCP stream and close the connection.
4. If the connection fails (e.g., Connection Refused), the program must write exactly the following SSH port forwarding command into a new file `/home/user/tunnel_cmd.sh`:
   `ssh -N -f -L 5555:metrics.internal:80 admin@bastion.host`

After writing the Rust program, compile it. Do not run it (the automated test will run it under different network and disk conditions to verify both the connection success and failure branches).

Ensure that:
- Your Rust code properly handles recursive directory traversal to sum file sizes.
- The compiled binary is located exactly at `/home/user/quota_monitor`.