You are a performance engineer tasked with profiling application latencies and building an anomaly detector for a microservice architecture.

Part 1: Multi-Service Configuration
We have a local stack simulating our production environment in `/home/user/app/`:
- Redis server
- Two Python Flask instances (API backends)
- Nginx (load balancer)

Currently, the services are not communicating correctly. 
1. Modify `/home/user/app/nginx.conf` so that it listens on port 8080 and load-balances HTTP requests round-robin to the two Flask instances on ports 5001 and 5002.
2. Modify `/home/user/app/api.py` so that it connects to the local Redis instance on port 6379 and pushes the request processing latency (a float) to the Redis list named `latency_metrics`.
3. Start the services by running `/home/user/app/start_services.sh`. Ensure you can make a GET request to `http://127.0.0.1:8080/ping` and see latencies appear in Redis.

Part 2: Anomaly Detection (Adversarial Corpus)
We have captured latency profiles (lists of floating-point numbers in JSON format) from various service runs. 
Healthy ("clean") services exhibit latencies that roughly follow an Exponential distribution.
Degraded ("evil") services exhibit heavy-tailed latencies or bimodal spikes due to GC pauses or lock contention.

You must write a Python script at `/home/user/profile_classifier.py` that takes a single CLI argument: the path to a JSON file containing an array of latencies.
The script must analyze the data and classify it:
- Exit with code `0` (Success) if the profile is HEALTHY (clean).
- Exit with code `1` (Error) if the profile is DEGRADED (evil).

To implement this, your script should use scientific computing techniques:
- Fit the data to an expected distribution or compute a probability distribution distance metric (e.g., Wasserstein distance, Kolmogorov-Smirnov test).
- Calculate bootstrap confidence intervals for a high percentile (e.g., 95th or 99th percentile) to determine if the tail is unexpectedly heavy.

The system will test your script against two directories:
- `/home/user/data/clean/`: Contains 50 healthy latency profiles. Your script must exit 0 for ALL of them.
- `/home/user/data/evil/`: Contains 50 degraded latency profiles. Your script must exit 1 for ALL of them.

Ensure your script processes a file within 2 seconds.