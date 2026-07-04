A backend Python service has been deployed on this server, but the frontend proxy is broken because it cannot connect to the backend's dynamically generated Unix domain socket. 

Your task is to fix this connection issue by creating a bridge between the network and the Unix socket.

Here is what you need to do:
1. The backend service writes its startup logs to `/home/user/service.log`. Inspect this log file using text processing tools to find the latest Unix socket path the service bound to. Look for a log entry resembling `[INFO] Backend listening on unix socket: <path>`.
2. Write a Python script at `/home/user/bridge.py`. This script must:
   - Listen for incoming TCP connections on `127.0.0.1` port `8888`.
   - Accept a connection, read all available incoming data, and forward it to the Unix socket you extracted from the log.
   - Read the response from the Unix socket and forward it back to the TCP client.
   - Close the connection.
3. Start your `/home/user/bridge.py` script in the background.
4. Verify the bridge works by sending the exact string `PING` to `127.0.0.1` on port `8888` (using `nc` or a similar tool).
5. Save the exact response received from the service to the file `/home/user/result.txt`.

Ensure your Python script correctly handles binary data and socket connections. The backend service is already running and waiting for input.