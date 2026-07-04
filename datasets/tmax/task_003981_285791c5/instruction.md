You are a network engineer troubleshooting a broken local microservice pipeline. The system consists of three Python services that simulate a data pipeline, but they are currently unable to communicate due to misconfigurations and network routing issues.

Your workspace is in `/home/user/microservices/`.
There are three services:
1. `emitter.py`: Generates data and sends it to the Processor.
2. `processor.py`: Receives data, processes it, and sends it to the Aggregator.
3. `aggregator.py`: Receives processed data and keeps statistics.

A configuration file exists at `/home/user/microservices/config.ini`.

Your task consists of the following phases:

**Phase 1: Idempotent Configuration Fix**
The `emitter.py` service is failing because it is configured to send data to the wrong port. The Processor listens on port `8002`, but the `[Emitter]` section in `config.ini` has `processor_port` set to `8080`.
Write a Python script at `/home/user/apply_fixes.py` that reads `/home/user/microservices/config.ini` and updates `processor_port` to `8002`. This script must be strictly idempotent (running it multiple times should result in the exact same file state and not corrupt the file). Execute the script to fix the config.

**Phase 2: Port Forwarding / Tunneling**
The Processor is hardcoded via the config to send data to the Aggregator on port `9003`. However, the Aggregator service actually binds to port `8003`. You are **not** allowed to modify `config.ini` for the Processor or Aggregator to fix this, nor can you modify the service code.
Instead, establish a local port forward so that traffic sent to `127.0.0.1:9003` is forwarded to `127.0.0.1:8003`. You may use `socat`, `ssh -L` (if you configure a local user-level sshd), or any other standard shell utility available to maintain this tunnel in the background.

**Phase 3: Service Startup and Text Processing**
Start the three services in the background (they are executable and use the current directory's config). The services log to `/home/user/microservices/logs/`.
Once the pipeline is flowing, `aggregator.log` will begin registering successful payloads in the format:
`[INFO] - SUCCESS - Transaction ID: <uuid> - Payload processed`

Write a shell command pipeline (using `grep`, `awk`, `sed`, etc.) that extracts *only* the UUID of the very first successful transaction from `/home/user/microservices/logs/aggregator.log`. Save this exact UUID string to a file at `/home/user/first_transaction.txt`.

**Phase 4: Robust Health Monitoring**
Write a Python script at `/home/user/monitor.py` that continuously polls the Aggregator's health endpoint: `GET http://127.0.0.1:8003/stats`.
The endpoint returns JSON like `{"total_received": X}`.
Your script must:
1. Handle connection errors and timeouts gracefully without crashing (using robust error handling).
2. Poll every 1 second until `total_received` is strictly greater than or equal to `5`.
3. Once this condition is met, write the exact JSON payload `{"status": "success", "count": 5}` to `/home/user/monitor_result.json` and exit successfully.
Run this script.