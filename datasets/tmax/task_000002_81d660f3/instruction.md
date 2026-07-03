You are a system administrator maintaining a custom microservices stack. We are deploying a local environment using user-level systemd services. 

Currently, the stack consists of three components:
1. An API server running on port 9001.
2. A local port forwarder (tunnel) that listens on port 9002 and forwards all TCP traffic to the API server on port 9001.
3. A load balancer running on port 9000 that routes traffic between port 9001 and port 9002. It performs a strict startup check and will immediately crash if either port 9001 or 9002 is not accepting connections.

We have a few problems you need to solve:

**Phase 1: Write the Tunnel**
The tunnel script is missing. Write a Python script at `/home/user/tunnel.py` that listens on `127.0.0.1:9002`. Whenever a client connects to it, it should open a connection to `127.0.0.1:9001` and bidirectionally forward all TCP traffic between the client and the API server. 

**Phase 2: Fix the Service Configuration**
I have created the systemd unit files in `/home/user/.config/systemd/user/`:
- `api.service`
- `tunnel.service`
- `lb.service`

However, if you try to start them all at once, `lb.service` crashes. It attempts to start before the `api` and `tunnel` services are fully up and bound to their ports. 
Modify `/home/user/.config/systemd/user/lb.service` to ensure it starts *strictly after* `api.service` and `tunnel.service`. Additionally, `lb.service` must *require* both of these services so they start automatically when `lb.service` is started. Note: you do not have root access, so use `systemctl --user` for all systemd commands.

**Phase 3: Verify the Setup**
Once you have written the tunnel script, fixed the systemd configuration, and successfully started `lb.service` (which should now automatically start the other two), write a Python script at `/home/user/verify.py` that sends exactly 4 HTTP GET requests to `http://127.0.0.1:9000/`. 
The script must append the exact HTTP response body of each request as a new line to `/home/user/test_results.log`.

Do not modify `api_server.py` or `lb.py`. Ensure your `tunnel.py` handles continuous traffic properly.