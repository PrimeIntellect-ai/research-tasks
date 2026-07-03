You are a deployment engineer responsible for rolling out an update to a Rust-based API gateway. The system uses a blue/green deployment strategy via directory symlinks. The gateway sits in front of a legacy backend Python service and sanitizes incoming JSON payloads.

Currently, the deployment is broken due to a network misconfiguration between the gateway and the upstream service, and the payload sanitizer lacks the correct filtering logic.

Your objectives:

1. **Implement the Payload Filter (Adversarial Corpus)**
   Navigate to `/home/user/gateway/payload_filter`. You must implement the logic in `src/main.rs` to parse a JSON file provided as the first CLI argument. 
   - Accept (exit code `0`) any valid JSON file (the "clean" payload).
   - Reject (exit code `1`) any JSON file that contains the exact key string `__proto__` anywhere in its structure, or any string value that contains the substring `<script>`.
   - Your solution will be tested against two hidden corpora: clean payloads and malicious/evil payloads.

2. **Fix the Multi-Service Compose Setup**
   The application environment is managed by a local startup script.
   - The backend service runs on `127.0.0.1:8081`.
   - The Rust gateway service (`gateway_server`) is supposed to bind to `127.0.0.1:8080` and route traffic to the backend.
   - Currently, the gateway is misconfigured and tries to route to the wrong port. Find its configuration file in `/home/user/gateway/config/settings.toml` and fix the routing mismatch so the gateway correctly forwards requests to the backend service.

3. **Construct the Deployment Pipeline**
   Write a deployment script at `/home/user/deploy.sh` (make it executable) that performs the following steps:
   - Builds the Rust workspace at `/home/user/gateway` in release mode.
   - Creates a new release directory at `/home/user/deploy/releases/$(date +%s)`.
   - Copies both compiled binaries (`gateway_server` and `payload_filter`) to this new release directory.
   - Backs up the target of the current active symlink (`/home/user/deploy/current`) by creating a text file `/home/user/deploy/backups/last_active.txt` containing the absolute path of the previous release directory. If the symlink doesn't exist yet, skip this backup step.
   - Updates the `/home/user/deploy/current` symlink to point to the new release directory.

Execute your `deploy.sh` script to deploy your fixed filter and gateway. Ensure that after deployment, you can successfully `curl http://127.0.0.1:8080/api` and receive a response from the upstream service.