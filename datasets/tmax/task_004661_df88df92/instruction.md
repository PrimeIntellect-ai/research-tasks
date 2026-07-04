You are a network engineer troubleshooting connectivity and performance issues for an internal microservices cluster. You need to set up a load balancer, manage backend processes, and run a load test to verify the throughput. However, the custom internal load testing tool is currently malfunctioning and reporting artificially low numbers.

Your task has three parts:

1. **Fix the Vendored Load Tester:**
   There is a Python load-testing package pre-vendored at `/app/vendored/netprobe-1.0.0`. It is supposed to send high-volume asynchronous requests, but a recent commit introduced a severe performance regression. Analyze the source code in `/app/vendored/netprobe-1.0.0/netprobe/client.py`, find the deliberate perturbation (e.g., a blocking sleep or incorrect timeout that ruins async performance), and fix it. Ensure the package is installed/usable in your environment.

2. **Automate Backend Lifecycle & Setup Load Balancer:**
   - Create a directory structure under `/home/user/services/` with subdirectories `logs/` and `run/`. Create a symlink from `/home/user/logs` pointing to `/home/user/services/logs`.
   - Write a Python automation script `/home/user/start_backends.py` that starts three separate HTTP backend servers on ports `9001`, `9002`, and `9003`. These can be simple Python `http.server` instances that return a 200 OK status. The script should save their PIDs to `/home/user/services/run/`.
   - Write a lightweight asynchronous Python reverse proxy `/home/user/proxy.py` that listens on port `8080`. It must load balance incoming HTTP requests across the three backend servers (ports 9001, 9002, 9003) using a simple round-robin approach. 

3. **Run the Verification:**
   Once your backends and reverse proxy are running, execute the fixed netprobe tool against your load balancer:
   `python3 -m netprobe --url http://127.0.0.1:8080 --duration 5 --output /home/user/probe_results.json`

Ensure your reverse proxy is efficient enough and the tool is fixed so that the system achieves a high throughput. The automated verification will extract the requests per second (RPS) from `/home/user/probe_results.json` and verify it meets the required performance threshold. Keep the proxy and backends running in the background when you complete the task.