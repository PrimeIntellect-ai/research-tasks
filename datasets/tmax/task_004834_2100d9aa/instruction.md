You are tasked with setting up a highly available, locally load-balanced mock Kubernetes operator API using process supervision, SSH tunneling, and a custom Python reverse proxy.

We have provided a proprietary, stripped binary at `/app/operator-core` that acts as the manifest management engine. 

Here are the requirements for the system:

1. **Reverse Engineer the API Auth:**
   The `/app/operator-core` binary runs an HTTP server. It accepts a `--port` argument. However, it requires a specific authentication header to accept requests to `/api/v1/manifests`. The header name is `X-K8s-Mock-Auth`, but the secret token value is hardcoded inside the stripped binary. You must analyze the binary to discover this token.

2. **Python Reverse Proxy & Load Balancer:**
   Write a Python script at `/home/user/proxy.py` that acts as an HTTP reverse proxy listening on `127.0.0.1:9090`.
   - The proxy must distribute incoming requests using a round-robin strategy across two backend instances of the `operator-core` binary running on `127.0.0.1:8081` and `127.0.0.1:8082`.
   - The proxy MUST automatically inject the `X-K8s-Mock-Auth` header (with the token you discovered) into all requests forwarded to the backends, so external clients do not need to provide it.

3. **Secure Exposure via SSH Tunnel:**
   External clients must access the proxy securely. You must set up local SSH port forwarding so that `0.0.0.0:8000` is forwarded to the Python proxy listening on `127.0.0.1:9090`.
   - You may need to generate an SSH keypair for the `user` and add it to `~/.ssh/authorized_keys` to allow passwordless `localhost` SSH access.

4. **Process Supervision:**
   The entire stack must be managed by `supervisord`. Create a configuration file at `/home/user/supervisor.conf` that defines and supervises the following programs:
   - `operator-1`: Runs `/app/operator-core --port 8081`
   - `operator-2`: Runs `/app/operator-core --port 8082`
   - `proxy`: Runs your `/home/user/proxy.py` script
   - `tunnel`: Runs the SSH tunnel command to expose port 8000
   
   Configure `supervisord` to automatically restart any failed processes. Once your configuration is ready, start `supervisord` in the background.

To verify your setup, we will send HTTP GET requests to `http://127.0.0.1:8000/api/v1/manifests` and ensure we receive successful responses distributed across both backend instances.