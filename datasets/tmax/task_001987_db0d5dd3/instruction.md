You are acting as a backup operator who needs to test the deployment and restoration of a legacy system service.

We have recovered a backup configuration document as an image file located at `/app/backup_config.png`.
Your objectives are:

1. **Extract Configuration**: Use OCR (tesseract is installed) to read the text from `/app/backup_config.png`. You will find a field labeled `AUTH_TOKEN: ` followed by a UUID. Extract this UUID.
2. **Git Server Setup**: Initialize a bare Git repository at `/home/user/deploy.git`. Clone it to `/home/user/workspace`.
3. **Write the Service**: Inside `/home/user/workspace`, write a C program named `server.c` that acts as a simple TCP server. It must bind to `127.0.0.1` on port `9090`. Whenever a client connects, the server should immediately send the extracted `AUTH_TOKEN` string (just the UUID, followed by a newline) and then close the connection.
4. **Task Automation via Git Hooks**: In the bare repository (`/home/user/deploy.git`), configure a `post-receive` hook. This hook must:
   - Checkout the latest code into a deployment directory at `/home/user/deployed_service`.
   - Compile `server.c` into an executable named `server_bin`.
   - Terminate any existing instance of `server_bin`.
   - Start the new `server_bin` in the background.
5. **Deployment**: Commit your `server.c` in the `/home/user/workspace` repository and push it to the `deploy.git` remote. The push should trigger your hook, compile the code, and start the TCP service.

Verify your setup by manually connecting to `127.0.0.1:9090` (e.g., using `nc`) and ensuring the correct token is returned. Leave the service running.