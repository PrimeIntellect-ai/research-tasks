You are an edge computing engineer deploying an IoT telemetry pipeline to a remote device. The deployment is currently failing due to orchestration issues and a missing security filter.

The application files are located in `/app/`. The pipeline consists of three services:
1. **Redis**: Message broker.
2. **Telemetry Receiver**: A Python Flask service (`/app/receiver.py`) that listens on port 5000 for incoming POST requests at `/telemetry`.
3. **Telemetry Worker**: A Python worker (`/app/worker.py`) that pops verified messages from Redis and writes them to `/app/output.log`.

Your tasks are:

**1. Fix the Service Orchestration**
The startup script `/app/start_services.sh` starts all three services simultaneously. Because the worker and receiver try to connect to Redis before it's fully initialized, they crash. This is similar to a missing `After=` systemd dependency. 
Modify `/app/start_services.sh` using shell utilities to ensure the script pauses until Redis is actively listening on TCP port 6379 before launching `receiver.py` and `worker.py`. 

**2. Configure the Environment**
The receiver needs a validation script to filter out malicious or malformed IoT payloads. Configure your shell environment (e.g., in `/home/user/.bash_profile` or via a `.env` file sourced by your fixed script) to export:
* `REDIS_URL="redis://127.0.0.1:6379/0"`
* `FILTER_SCRIPT="/home/user/telemetry_filter.py"`

**3. Implement the Adversarial Filter**
IoT botnets are sending malformed data. Create the script `/home/user/telemetry_filter.py` (ensure it is executable). The Flask receiver will execute this script, passing the incoming JSON payload via standard input (stdin).
The script must exit with status `0` if the payload is completely valid, and exit with status `1` (or any non-zero) if it is invalid/malicious.

A valid telemetry payload MUST strictly meet these criteria:
* It is valid JSON containing exactly three top-level keys: `device_id`, `timestamp`, and `metrics`. Any extra keys (e.g., `cmd`, `debug`) must be rejected.
* `device_id` must be a string matching the exact regex pattern: `^DEV-\d{4}$`
* `timestamp` must be an integer.
* `metrics` must be a JSON object (dictionary) where all keys are strings and all values are numbers (integers or floats).
* Inside `metrics`, if the key `temperature` exists, its value must be between `-50.0` and `100.0` (inclusive). Anything outside this range is a sensor spoofing attack.

**4. Run the Pipeline**
Execute your fixed `/app/start_services.sh` so the services are running in the background. Do not terminate them. 

Once running, an automated verifier will test your pipeline by sending hundreds of payloads from a clean corpus and an evil corpus to `http://127.0.0.1:5000/telemetry`. All valid payloads must end up processed by the worker, and all malicious payloads must be rejected by your filter.