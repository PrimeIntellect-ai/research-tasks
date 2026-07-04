You are a cloud architect tasked with migrating a legacy data service to a new Go-based deployment. Due to a previous network misconfiguration in a staged rollout, direct external access to the legacy service was severed, and you must now write a proxy layer.

You have been provided with a legacy, stripped binary located at `/app/legacy_api`. 
Your objective is to integrate this legacy binary with a new Go service and deploy both using a custom bash supervisor.

Here are your requirements:

1. **Analyze the Legacy Binary**:
   - The binary `/app/legacy_api` is stripped. You must determine its expected environment and behavior. 
   - *Hint:* The binary requires specific locale and timezone configurations to start successfully (specifically `TZ=UTC` and `LC_ALL=C`). 
   - It binds to a local port and exposes a specific HTTP endpoint that returns a secret migration token. You will need to reverse-engineer or black-box inspect it to find the port and the exact path (e.g., `/token` or similar).

2. **Write the Go Proxy Service**:
   - Create a Go program at `/home/user/proxy.go` and compile it to `/home/user/proxy`.
   - Your Go service must run two concurrent servers:
     - An **HTTP Server** listening on `0.0.0.0:8080`. When a client makes a `GET /legacy-status` request, your Go service must forward the request to the legacy binary's hidden token endpoint and return the exact response body to the client with a 200 OK status.
     - A **TCP Healthcheck Server** listening on `0.0.0.0:8081`. When a client connects via raw TCP, the server must immediately send the exact string `HEALTHY\n` and close the connection.

3. **Implement Process Supervision and Quota Management**:
   - Create a bash script at `/home/user/supervise.sh`.
   - The script must start both `/app/legacy_api` (with the correct environment variables) and your `/home/user/proxy` in the background.
   - It must implement a **restart policy**: if either process crashes or is killed, the script must automatically restart it within 2 seconds.
   - Both processes must append their stdout and stderr to `/home/user/logs/app.log` (ensure the `/home/user/logs` directory is created).
   - The script must implement basic **storage monitoring**: a background loop must check the size of `/home/user/logs/app.log` every 3 seconds. If the file size exceeds 500 KB, the script must truncate the file to 0 bytes to prevent disk exhaustion.

4. **Execution**:
   - Run your `/home/user/supervise.sh` script so that all services are bound and listening. Leave the processes running so the automated verifier can test the endpoints.