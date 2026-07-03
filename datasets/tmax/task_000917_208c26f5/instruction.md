You are a container specialist managing a local microservices stack. We have a set of services running under `/home/user/app/` that need to be glued together, stabilized, and protected against malicious metric-poisoning attacks.

There are three microservices:
1. **Nginx API Gateway**: Listens on `127.0.0.1:8080`. Forwards requests to a local metric aggregator.
2. **Flask Metric Aggregator**: Runs on `127.0.0.1:5000`. Expects to write to a Redis backend.
3. **Redis Datastore**: Runs on `127.0.0.1:6379`.

However, the architecture has a few critical flaws that you need to resolve:

**Step 1: Storage and Mount Setup**
The Flask app expects its configuration to be available at `/home/user/app/config_mount`. You must mount the directory `/home/user/app/config_source` to `/home/user/app/config_mount` using `bindfs` (which is installed and works without root). Create a user-level systemd service named `app-mount.service` in `/home/user/.config/systemd/user/` that automatically performs this mount on startup and unmounts on stop. 

**Step 2: Service Connectivity via SSH Tunneling**
The Redis datastore is actually locked down and only accepts connections locally, but for architectural reasons, the Flask app is configured to connect to Redis at `127.0.0.1:9000`. Set up an SSH tunnel that forwards `127.0.0.1:9000` to `127.0.0.1:6379` using the local user's SSH keys (assume key generation and `authorized_keys` setup is already done for `user@localhost`). Create another user-level systemd service `redis-tunnel.service` to manage this persistent tunnel.

**Step 3: Adversarial Metric Filter (Go)**
Our Nginx gateway receives metric payloads (JSON) from external clients, but we are being hit with metric poisoning attacks. You must write a Go program at `/home/user/app/filter/main.go` that acts as a CLI sanitizer. 
It will read line-by-line JSON objects from Standard Input. 
If the payload is clean, it must print the exact original JSON line to Standard Output. 
If the payload is malicious, it must NOT print anything for that line (skip it).

A malicious payload is defined as any JSON object where:
- The `metric_value` field is negative.
- The `metric_name` contains the substring `DROP_TABLE` or `SCRIPT_TAG`.
- The `tags` array contains any string exceeding 50 characters.

**Step 4: End-to-End Integration and Health Check**
Compile your Go program to `/home/user/app/filter/metric_filter`.
Then, start the multi-service compose stack using the provided script at `/home/user/app/start_services.sh`. Ensure your systemd services (`app-mount.service` and `redis-tunnel.service`) are enabled and running. 
Finally, verify the pipeline by running a test script (which you don't need to write, we will run it during evaluation) that pushes data through Nginx -> Filter -> Flask -> Redis.