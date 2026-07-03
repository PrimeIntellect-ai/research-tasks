You are an operations engineer debugging a local development environment. The development team has set up three backend API instances using Docker Compose and a local Nginx load balancer managed by a systemd user service. However, the load balancer service fails to start, and the traffic benchmarking tool shows a complete failure.

Your objective is to diagnose and fix the infrastructure so that the load balancer correctly distributes traffic across all three backend containers, and then run the benchmarking tool to verify performance.

Here is the setup:
- **Docker Compose Setup**: Located at `/home/user/backend/docker-compose.yml`. It defines three backend containers.
- **Reverse Proxy**: An Nginx configuration is located at `/home/user/proxy/nginx.conf`. It is supposed to listen on `127.0.0.1:8080` and load-balance requests across the three backends.
- **Service Management**: A systemd user service is located at `/home/user/.config/systemd/user/local-proxy.service`. It is meant to manage the Nginx proxy.

Issues to resolve:
1. The backends in the `docker-compose.yml` are not reachable from the host because their ports are configured incorrectly. Fix the compose file so the three backends map their internal port `80` to the host ports `8001`, `8002`, and `8003`. Restart the containers.
2. The `local-proxy.service` fails to start due to a misconfiguration in the systemd unit file and a syntax error in `nginx.conf`. Diagnose and fix these files.
3. Start the systemd service successfully (`systemctl --user start local-proxy.service`).
4. Once the proxy is running and correctly load balancing across all three backends, run the traffic generation and benchmarking binary located at `/app/lb_bench`. 

The benchmarking tool `/app/lb_bench` requires no arguments. It will automatically send requests to `http://127.0.0.1:8080/`, measure the Requests Per Second (RPS), and count the number of unique backends that served the requests. 
It outputs the results in JSON format to `stdout`.

Capture the exact output of `/app/lb_bench` and save it to `/home/user/bench_results.json`. Ensure the setup allows the benchmark to see all 3 unique backends and achieve a high RPS.