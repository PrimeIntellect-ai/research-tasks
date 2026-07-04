You are a deployment engineer tasked with rolling out a new automated update gateway. The system relies on a central Rust service that authenticates requests, verifies user roles, and triggers a deployment routine inside an isolated Virtual Machine using an `expect` script.

Your objective is to complete the deployment gateway by integrating several components:

1. **Extract Configuration:**
   An architecture diagram with embedded deployment parameters is located at `/app/deploy_config.png`. Use OCR (e.g., `tesseract`) to read the image. You will find a deployment authorization token (labeled "AUTH_TOKEN:") and a TCP port number (labeled "PORT:").

2. **User Administration Config:**
   The gateway validates users via a local JSON file. Create a file at `/home/user/roles.json` containing a list of users and their groups. You must create a user named `release_bot` and assign it to the `deployment_admins` group. The format must be exactly:
   ```json
   {
     "users": {
       "release_bot": { "group": "deployment_admins" }
     }
   }
   ```

3. **Expect Script for VM Management:**
   Write an `expect` script at `/home/user/deploy.exp`. When executed, this script must:
   - Spawn the mock QEMU serial console located at `/app/vm_console.sh`.
   - Wait for the string `login: ` and send the username `admin` followed by a newline.
   - Wait for the string `Password: ` and send `root123` followed by a newline.
   - Wait for the prompt `root@vm:~# ` and send the command `touch /opt/deploy_success.flag` followed by a newline.
   - Wait for the prompt `root@vm:~# ` again, send `exit` followed by a newline, and terminate cleanly.

4. **Rust Gateway Service:**
   Create a pure Rust HTTP server in a new Cargo project at `/home/user/gateway`. You may use standard libraries (`std::net::TcpListener`) to avoid heavy dependency compilation.
   - The service must bind to `127.0.0.1` on the port extracted from the image.
   - It must accept `POST /deploy` requests.
   - It must require an `Authorization: Bearer <AUTH_TOKEN>` header matching the token from the image. If missing or invalid, return `401 Unauthorized`.
   - The request body will be JSON like `{"username": "release_bot"}`. The Rust service must parse this, check `/home/user/roles.json` to ensure the user is in the `deployment_admins` group. If not, return `403 Forbidden`.
   - If authorized, the Rust service must execute your `/home/user/deploy.exp` script using `std::process::Command`.
   - Upon successful execution of the expect script (exit code 0), return a `200 OK` HTTP response with the body `{"status": "deployed"}`.

Leave the Rust service running in the background when you are finished so it can be verified.