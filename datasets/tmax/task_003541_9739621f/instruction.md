You are an infrastructure engineer tasked with automating the provisioning and repair of a legacy backend service and its Nginx reverse proxy. 

A previous engineer left the provisioning half-finished. The Nginx reverse proxy is currently returning a 502 Bad Gateway because it is configured to forward requests to the wrong Unix socket path. The correct configuration details were lost in a system crash, but a scanned copy of the original provisioning sheet was recovered as an image.

Your objective is to complete the setup, fix the configuration, and bring the service online reliably.

Here is your workflow:

1. **Information Recovery (OCR):**
   Examine the recovered image located at `/app/config_snapshot.png`. You will need to extract two pieces of information from this image:
   - The correct "Backend Socket" path.
   - The "Init PIN" required to initialize the backend service.
   *(Hint: `tesseract` is installed on this system.)*

2. **Pre-modification Backup:**
   Before making any changes or running initializations, securely back up the entire `/app/backend/` directory. Create a compressed tar archive at `/app/backup/backend_backup.tar.gz` that preserves all original file permissions and ownerships.

3. **Service Initialization (Interactive Automation):**
   The backend service requires an interactive initialization process via the script `/app/backend/init.sh`. This script prompts for the "Init PIN".
   Write an `expect` script (e.g., `/app/automate_init.exp`) to programmatically run `/app/backend/init.sh` and supply the exact PIN you recovered from the image. Successful initialization will generate an authorization token locally in the backend directory.

4. **Service Provisioning & Permissions:**
   The backend application is a Python script located at `/app/backend/server.py`. Start this service in the background, passing the correct socket path (recovered from the image) as an argument:
   `python3 /app/backend/server.py --socket <CORRECT_SOCKET_PATH>`
   
   Once the service creates the Unix socket, you must ensure that the Nginx worker processes can read and write to it. Modify the permissions of the newly created Unix socket to `666` (read/write for all) so that the proxy can communicate with the backend.

5. **Nginx Reverse Proxy Fix:**
   An Nginx configuration file is located at `/app/nginx/nginx.conf`. 
   - Inspect it and locate the upstream definition that is currently pointing to a `wrong.sock` path.
   - Update this file to use the exact correct socket path recovered from the image.
   - Start the Nginx instance as a non-root user using this specific configuration directory:
     `nginx -p /app/nginx -c nginx.conf`

Once complete, the Nginx server should be listening locally on the port defined in its configuration, properly routing requests to the Python backend via the correct Unix socket. You can test your setup by making an HTTP GET request to `http://127.0.0.1:8080/status`.