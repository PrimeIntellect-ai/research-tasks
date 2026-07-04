You are an infrastructure engineer tasked with automating the deployment of a secure local gateway for virtual machine metrics. You need to write a Python provisioning script that parses a VM configuration file, generates necessary SSL certificates, prepares a metrics payload based on standard QEMU VNC port mappings, and generates a standalone secure web server script.

Your objective is to create a single Python script at `/home/user/provision.py`. When run, this script must perform the following tasks:

1. **Parse Configuration:** 
   Read a system configuration file located at `/home/user/vm.conf`. This file uses a simple `KEY=VALUE` format. It will contain (at minimum) `VM_NAME` and `VNC_DISPLAY` (e.g., `VNC_DISPLAY=:5`).

2. **Calculate Port:**
   Calculate the actual TCP port used by the VM's VNC server. QEMU and standard VNC servers map display numbers to ports starting at 5900 (e.g., display `:5` corresponds to port 5905).

3. **Generate SSL Certificates:**
   Create a directory `/home/user/ssl/` if it doesn't exist. Use Python's `subprocess` module to call `openssl` and generate a self-signed RSA certificate and private key. Save them as `/home/user/ssl/cert.pem` and `/home/user/ssl/key.pem` respectively. Configure them to be valid for at least 30 days with a Common Name (CN) of `localhost`.

4. **Prepare Metrics File:**
   Create a directory `/home/user/web/` if it doesn't exist. Write a JSON file to `/home/user/web/metrics.json` with the following exact keys and values parsed/calculated from the config:
   ```json
   {
       "vm": "<parsed_vm_name>",
       "vnc_port": <calculated_integer_port>,
       "status": "running"
   }
   ```

5. **Generate Web Server Script:**
   Write a Python script to `/home/user/gateway.py`. This generated script, when executed, must:
   - Change its current working directory to `/home/user/web/`.
   - Start an `http.server` running on `127.0.0.1` at port `8443`.
   - Wrap the server socket with Python's `ssl` module using the certificate and key generated in `/home/user/ssl/`, so that it serves files over HTTPS.

**Constraints & Verification:**
- Do not start the `gateway.py` server within `provision.py`. Our automated tests will run `python3 /home/user/provision.py`, followed by starting `/home/user/gateway.py` in the background, and will verify the deployment by fetching the JSON file using `curl -k https://127.0.0.1:8443/metrics.json`.
- Ensure your `provision.py` script is executable or can be run cleanly with `python3 /home/user/provision.py`.
- Ensure directories are created with appropriate permissions.