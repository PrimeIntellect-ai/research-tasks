You are an edge computing engineer configuring a secure local ingestion point for an IoT gateway device. You need to create an automated setup that handles configuration generation via a C utility, sets up a local web server, and wraps it in a TLS layer using user-space port forwarding. 

Since you do not have root access on this gateway, you must use high ports.

Perform the following steps:

1. **Directories**: Create the directories `/home/user/certs` and `/home/user/edge_data`.

2. **TLS Configuration**: Generate a self-signed RSA 2048-bit certificate and unencrypted private key. Place them at `/home/user/certs/edge.crt` and `/home/user/certs/edge.key`. Use `localhost` as the Common Name (CN).

3. **Interactive C Utility**: Write a C program at `/home/user/iot_setup.c`. 
   - When executed, it should read exactly two lines from standard input (stdin).
   - The first line represents the `Device ID` (max 50 chars).
   - The second line represents the `Sensor Type` (max 50 chars).
   - It must then create and write to a file at `/home/user/edge_data/config.json` with the exact following JSON format:
     `{"device_id": "<ID>", "sensor": "<TYPE>"}`
   - Ensure the newline characters are stripped from the input strings before writing the JSON.

4. **Deployment Script**: Write a bash script at `/home/user/deploy.sh` and make it executable. The script must perform the following actions in order:
   - Compile `/home/user/iot_setup.c` into an executable at `/home/user/iot_setup`.
   - Execute `/home/user/iot_setup` and automatically feed it the inputs `"Gateway-Alpha"` (for Device ID) and `"Humidity"` (for Sensor Type).
   - Start a Python HTTP server in the background listening on port `8080`, serving the files located in the `/home/user/edge_data` directory.
   - Start a `socat` process in the background that listens for incoming TLS connections on TCP port `8443` and forwards them to TCP `localhost:8080`. It must use the certificate and key generated in step 2 (e.g., using `openssl-listen`). Ensure the `socat` TLS listener disables certificate verification for incoming clients (`verify=0`).
   - Write the Process IDs (PIDs) of the backgrounded Python server and `socat` processes to a file at `/home/user/run.log` in the exact format:
     ```
     PYTHON_PID=<pid>
     SOCAT_PID=<pid>
     ```

5. **Execution**: Run your `/home/user/deploy.sh` script so that the services are actively running in the background and the `run.log` and `config.json` files are generated.