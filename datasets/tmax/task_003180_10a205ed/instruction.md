You are a container specialist managing a simulated microservices environment. We are experiencing a network misconfiguration where our API services cannot reach our email notification service, and we lack a load balancer to distribute traffic across our API replicas.

Your task is to fix the configuration, implement a custom Python-based reverse proxy / load balancer, and automate the verification.

Here is the current system state:
- There is a configuration file at `/home/user/microservices/config.json`. It specifies the ports for the services.
- The email service is hardcoded to listen on port `8025` when it starts, but `config.json` currently incorrectly lists the `email_port` as `9025`.
- Two instances of the API service are intended to run on the ports specified in `config.json` under the `api_ports` array (`8081` and `8082`).

Perform the following steps:

1. **Fix the Configuration:**
   Modify `/home/user/microservices/config.json` so that the `email_port` is correctly set to `8025`. Do not change the other configuration values.

2. **Implement the Reverse Proxy and Load Balancer:**
   Write a Python script at `/home/user/router.py` that acts as a simple HTTP reverse proxy listening on port `8080`. The script must use only standard Python libraries (e.g., `http.server`, `urllib.request`) and must:
   - Route any incoming HTTP GET request with the path `/api` to the API services. It must load-balance between the two API ports (`8081` and `8082`) using a strict Round-Robin strategy (first request to `8081`, second to `8082`, third to `8081`, etc.).
   - Route any incoming HTTP GET request with the path `/email` directly to the email service on port `8025`.
   - Forward the exact response body received from the underlying service back to the client with an HTTP 200 status code.

3. **Start the Services:**
   We have provided a script at `/home/user/microservices/start_services.py`. Run this script in the background. It will read `config.json`, start the email service on port `8025`, and start two API services on ports `8081` and `8082`. Once it is running, start your `/home/user/router.py` script in the background.

4. **Verify and Log:**
   Write a bash script at `/home/user/verify.sh` that performs the following exact `curl` requests in order, appending the output of each directly to `/home/user/routing.log` (do not add newlines between the outputs unless the service itself returns them):
   - `curl -s http://localhost:8080/api`
   - `curl -s http://localhost:8080/api`
   - `curl -s http://localhost:8080/email`

Run your `verify.sh` script to generate the final `/home/user/routing.log` file.