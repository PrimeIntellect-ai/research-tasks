You are tasked with deploying a hardened, custom backup aggregation daemon. We are migrating away from an off-the-shelf solution to a bespoke C-based service to improve our security posture and strictly control our backup endpoints.

First, analyze the legacy architectural diagram located at `/app/arch_diagram.png`. You will need to extract two critical pieces of configuration from this image:
1. The TCP listening port designated for the backup daemon.
2. The Vault Access Token required to authenticate incoming backup streams.

Next, implement the backup service by writing a C program at `/home/user/backup_daemon.c`. 
The daemon must adhere to the following specifications:
- It must bind to `127.0.0.1` on the port extracted from the image.
- It must accept raw TCP connections.
- The custom protocol requires clients to send data in exactly this format (terminated by a newline):
  `TOKEN:<vault_token_from_image>|PAYLOAD:<backup_data>\n`
- If the token exactly matches the one from the image, the server must:
  1. Write the `<backup_data>` string to a new file in `/home/user/backups/` (you can name the files sequentially or via timestamp, e.g., `backup_1.dat`).
  2. Send the response `OK\n` back to the client.
  3. Close the connection.
- If the token does not match or the format is malformed, the server must:
  1. Send the response `ERR: Unauthorized\n` back to the client.
  2. Close the connection.
- The server should run continuously, accepting connections one after another (or concurrently).

Finally, create a service lifecycle management script at `/home/user/manage_backup.sh`.
The script must take a single argument: `start` or `stop`.
- `./manage_backup.sh start` must:
  1. Compile `/home/user/backup_daemon.c` to `/home/user/backup_daemon`.
  2. Create the `/home/user/backups/` directory if it does not exist.
  3. Launch the compiled daemon in the background.
  4. Save the PID of the daemon to `/home/user/backup_daemon.pid`.
- `./manage_backup.sh stop` must:
  1. Read the PID from `/home/user/backup_daemon.pid`.
  2. Kill the running daemon.
  3. Remove the PID file.

Once you have written the code and the script, execute `./manage_backup.sh start` so that the service is running in the background. Do not stop the service at the end of your interaction; it needs to remain running for external verification.