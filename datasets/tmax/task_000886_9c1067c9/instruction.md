You are an infrastructure engineer automating the provisioning of a multi-protocol monitoring gateway. We have lost the original configuration file for our legacy gateway, but we have a screenshot of the configuration stored at `/app/config.png`.

Your task is to recreate the gateway and its supervision infrastructure.

Follow these steps:
1. **Extract Configuration**: Read the image file `/app/config.png` (using an OCR tool like `tesseract`) to extract three configuration values: the HTTP port, the TCP port, and a secret token.
2. **Directory Structure**: Create a directory at `/home/user/logs/` to store the application logs.
3. **Multi-Protocol Gateway**: Write a Python script at `/home/user/gateway.py` (using `asyncio`, `socket`, or `http.server` as you see fit) that starts two concurrent network services bound to `127.0.0.1`:
   - **HTTP Service**: Listens on the extracted HTTP port. It must expose a `GET /health` endpoint. If the request includes the HTTP header `Authorization: Bearer <TOKEN>` (where `<TOKEN>` is the token extracted from the image), it must respond with an HTTP 200 status code and the JSON payload `{"status": "ok"}`. If the token is missing or incorrect, it must return an HTTP 401 status code.
   - **TCP Echo Service**: Listens on the extracted TCP port. Any text line sent to this TCP socket must be echoed back to the client with the string `ACK: ` prepended. For example, if a client sends `ping\n`, the server should respond with `ACK: ping\n`. The connection should remain open until the client closes it.
4. **Process Supervision**: Write a bash script at `/home/user/supervise.sh` that acts as a process supervisor for `gateway.py`. The script must:
   - Execute the Python script.
   - Redirect all standard output and standard error from the Python script to `/home/user/logs/gateway.log`.
   - Monitor the Python process and immediately restart it if it crashes or exits.
5. **Execution**: Make sure your scripts are executable (`chmod +x`). Start `/home/user/supervise.sh` in the background so that the gateway services are actively running and listening on the ports. 

Our automated verification suite will issue real HTTP and TCP requests to the ports specified in the image to verify your implementation.