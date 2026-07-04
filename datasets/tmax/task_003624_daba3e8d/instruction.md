You are tasked with building a custom, lightweight "Manifest Operator" in C that simulates Kubernetes manifest synchronization, and setting up a basic infrastructure around it.

Because we are working in an unprivileged container environment, all processes must run as the default `user` and use unprivileged ports (>1024).

Your objectives are:

1. **Write the Operator (C Language):**
   Write a C program located at `/home/user/operator.c` and compile it to `/home/user/operator`. 
   - The program must accept a single command-line argument: a port number to listen on.
   - It should listen for incoming TCP connections on `127.0.0.1` on the specified port.
   - Whenever a connection is received (you can assume simple HTTP GET requests from `curl`), it must perform a "sync":
     - Read the directory `/home/user/manifests/`.
     - For every file ending in `.yaml`, create a corresponding "mail spool" file in `/home/user/mail_spool/` named `<filename>.processed` (e.g., if `app.yaml` is found, create `app.yaml.processed`).
     - The contents of this processed file must be exactly: `Processed <filename>` (e.g., `Processed app.yaml`). If the file already exists, overwrite it.
     - Respond to the TCP client with a valid minimal HTTP response: `HTTP/1.1 200 OK\r\n\r\nOK\n` and close the connection.
   - The program must keep running and listening for new connections after serving a request.

2. **Run Operator Instances:**
   Start two instances of your compiled `operator` program in the background, listening on ports `8081` and `8082`.

3. **Configure Reverse Proxy:**
   Write an HAProxy configuration file at `/home/user/haproxy.cfg`.
   - Configure a frontend listening on `127.0.0.1:8080`.
   - Configure a backend that load-balances (round-robin) between your two operator instances at `127.0.0.1:8081` and `127.0.0.1:8082`.
   - Start HAProxy in the background using this configuration (`haproxy -f /home/user/haproxy.cfg -D`).

4. **Create CI/CD Automation Script:**
   Write a bash script at `/home/user/cicd.sh` that simulates a deployment pipeline. The script must:
   - Create a file `/home/user/manifests/deployment.yaml` with the text `kind: Deployment`.
   - Trigger the operator by making an HTTP request to the HAProxy load balancer: `curl -s http://127.0.0.1:8080/sync`
   - Ensure the script is executable (`chmod +x /home/user/cicd.sh`).

The automated test will execute `/home/user/cicd.sh` and verify that the reverse proxy correctly routes the request, the C operator executes the filesystem logic, and the correct spool files are generated.