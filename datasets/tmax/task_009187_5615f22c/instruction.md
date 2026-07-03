You are an edge computing engineer deploying a new application to a fleet of IoT devices. The devices run a minimal Linux environment without root access, so you must implement network routing, firewalling, and process management in user space using Python.

There is an existing sensor data server located at `/home/user/sensor_server.py`. You need to write a Python script at `/home/user/edge_proxy.py` that acts as a secure edge gateway, port forwarder, process supervisor, and logger.

Write `/home/user/edge_proxy.py` to meet the following requirements:

1. **Process Supervision & Lifecycle Management**:
   - When executed, your script must launch the sensor server as a child process: `python3 /home/user/sensor_server.py`
   - If your `edge_proxy.py` script receives a `SIGTERM` signal, it must cleanly terminate the child `sensor_server.py` process before exiting itself.

2. **Port Forwarding**:
   - Your script must listen for incoming TCP connections on `127.0.0.1:8888`.
   - Any valid incoming connection must have its data forwarded to the sensor server, which is listening on `127.0.0.1:9090`. Responses from the sensor server must be forwarded back to the client on port 8888. (You can handle one connection at a time, or use threading/async, but simple synchronous handling of individual requests is sufficient for this IoT environment).

3. **Application-Layer Firewall**:
   - Before forwarding data, read the first 1024 bytes of the incoming connection.
   - If the incoming payload contains the exact string `BANNED_DEVICE`, your script must immediately close the connection without forwarding anything to port 9090.
   - Otherwise, forward the data to port 9090 and return the response.

4. **Log Configuration & Rotation**:
   - You must log firewall events. Specifically, whenever a connection is blocked due to the `BANNED_DEVICE` string, append a log line to `/home/user/proxy.log`.
   - The log entry must be exactly: `FIREWALL - Blocked connection` (you can include a timestamp via standard logging formatting, but the message itself must be exactly this).
   - You must use Python's built-in `logging` module with a `RotatingFileHandler`. Set `maxBytes=200` and `backupCount=1`.

The automated test will evaluate your script by running it, sending both valid and banned payloads to port 8888, verifying log rotation (`proxy.log` and `proxy.log.1`), and sending a `SIGTERM` to ensure the child process is cleaned up.