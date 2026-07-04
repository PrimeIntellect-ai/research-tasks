You are a Site Reliability Engineer tasked with setting up a resilient, security-filtered reverse proxy to protect and monitor our internal API backends.

Two identical backend Python API services are already running on your machine:
- Backend A: `127.0.0.1:8081`
- Backend B: `127.0.0.1:8082`

Your task is to write a Python-based reverse proxy script at `/home/user/proxy.py` that listens on `127.0.0.1:8080`. This proxy must act as both a load balancer and a Web Application Firewall (WAF), combining robust script writing, network forwarding, and timezone handling.

Requirements for `/home/user/proxy.py`:
1. **Load Balancing & Robustness**: Forward incoming HTTP GET requests to the backends using a round-robin strategy. If the chosen backend refuses the connection or times out, the proxy must catch the error and automatically retry with the other backend. 
2. **Adversarial WAF Filter**: Inspect the request path and query string. You must immediately reject the request and return an HTTP `403 Forbidden` status if the URI contains any of the following malicious patterns (case-insensitive):
   - `union select`
   - `<script>`
   - `../`
   - `eval(`
3. **Timezone Configuration**: For every request forwarded to a backend, inject a new HTTP header called `X-Proxy-Time`. The value must be the current time in the `Europe/Berlin` timezone, formatted exactly as `YYYY-MM-DD HH:MM:SS`.
4. **Execution**: Start your proxy script in the background so it is actively listening on port 8080. Save the process ID (PID) of your running proxy script to `/home/user/proxy.pid`.

We have provided two directories containing test URIs:
- `/home/user/corpus/clean/`: Contains files with benign request URIs.
- `/home/user/corpus/evil/`: Contains files with malicious request URIs.

An automated test suite will read the contents of the files in these directories and send HTTP GET requests to `http://127.0.0.1:8080<URI>`. 

For you to pass the task:
- 100% of the requests using URIs from the `clean` corpus must be routed to the backends and return a `200 OK` status code.
- 100% of the requests using URIs from the `evil` corpus must be blocked by your proxy and return a `403 Forbidden` status code.
- The `X-Proxy-Time` header must be correctly populated for all forwarded requests.

Ensure your proxy is running and `/home/user/proxy.pid` is created before you finish the task.