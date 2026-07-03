You are an edge computing engineer deploying a new telemetry ingestion pipeline for IoT devices on a local factory network. 

Your task consists of three parts: decoding an automated audio alert, building a telemetry validator, and scripting a rolling deployment.

**1. Audio Decoding (Deployment ID)**
An automated gateway has left an audio distress signal containing DTMF (touch-tone) digits in `/app/alert.wav`. 
You must decode these digits. The decoded sequence of numbers will act as your `$DEPLOY_ID`. 

**2. Telemetry Validator (Adversarial Corpus)**
IoT devices send JSON telemetry files. Some devices are malfunctioning or compromised and are sending malformed or malicious payloads.
Write a robust Bash script at `/home/user/verify_telemetry.sh` that takes a single argument (the path to a JSON file).
The script must act as a strict filter:
- Exit `0` (Accept) if the JSON file meets ALL the following criteria:
  - The `device_id` field exists and contains ONLY alphanumeric characters and hyphens (`A-Z`, `a-z`, `0-9`, `-`).
  - The `temperature` field exists, is a valid number, and is strictly between `-50` and `150` (inclusive).
- Exit `1` (Reject) if the file violates any of these rules, contains shell metacharacters, is malformed, or has missing fields.

**3. Staged Deployment Script**
Write a Bash script at `/home/user/deploy.sh` that performs the following actions:
1. Performs a connectivity diagnostic by checking if `127.0.0.1` is reachable via `ping` (1 packet). If not, exit with an error.
2. Creates a staging directory at `/home/user/deployments/$DEPLOY_ID/` (using the ID you extracted in step 1).
3. Iterates over all `.json` files in `/app/incoming/`. Uses your `/home/user/verify_telemetry.sh` script to test each file.
4. If a file is valid, copies it into the staging directory.
5. Performs a rolling deployment by creating or updating a symlink at `/home/user/current_telemetry` to point to the new `/home/user/deployments/$DEPLOY_ID/` directory.

Ensure your scripts handle edge cases cleanly without failing unexpectedly.