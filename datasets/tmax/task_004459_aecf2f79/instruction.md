You are acting as a DevSecOps engineer tasked with enforcing policy-as-code for a newly deployed log processing and analysis pipeline. 

The application architecture consists of three cooperating services located in `/home/user/app/`:
1. **API Gateway (Flask - Python):** Listens on port 8080. Receives encoded log payloads via HTTP POST on `/submit`.
2. **Message Broker (Redis):** Listens on port 6379. Buffers incoming payloads.
3. **Policy Enforcement Worker (Node.js):** Processes messages from Redis, decodes them, and forwards clean messages to an archive directory while rejecting malicious ones.

Currently, the services are not properly integrated, and the Policy Enforcement Worker lacks the logic to detect malicious payloads. 

Your tasks are as follows:

**Phase 1: Multi-Service Integration**
1. Review the configuration files in `/home/user/app/config/`.
2. Modify the Flask API (`/home/user/app/api/gateway.py`) to correctly connect to the Redis broker using the environment variables defined in `/home/user/app/config/broker.env`.
3. Modify the Node.js worker (`/home/user/app/worker/enforcer.js`) to pull from the `log_queue` in Redis.
4. Ensure the start-up script `/home/user/app/start.sh` successfully brings up all three services without crashing. Set appropriate file permissions on `/home/user/app/archive/` so only the worker process can write to it.

**Phase 2: Payload Decoding & Policy Enforcement**
The payloads submitted to the API are Base64 encoded JSON objects. You must implement a sanitization and detection function within the Node.js worker (`/home/user/app/worker/enforcer.js`). 
You must filter out payloads that contain malicious strings or violate Content Security Policy (CSP) rules (e.g., inline scripts, unauthorized external domains in the log metadata).
1. Decode the Base64 payload.
2. Verify the file integrity checksum provided in the JSON wrapper (SHA-256 of the decoded log field). If the checksum is invalid, reject it.
3. Write a classifier function: `function classifyPayload(decodedJson)` that returns `true` (clean) or `false` (evil).
4. Save clean logs to `/home/user/app/archive/<id>.json`.

**Phase 3: Adversarial Corpus Evaluation**
We have provided two corpora of raw JSON logs in `/home/user/corpora/`:
- `/home/user/corpora/clean/`: Contains safe, valid logs.
- `/home/user/corpora/evil/`: Contains logs with embedded CWEs (e.g., XSS payloads, SQLi strings, invalid CSP directives, or forged integrity checksums).

To verify your solution, we will run a test script that submits both corpora through your configured API Gateway. 

Write a CLI wrapper for your classifier at `/home/user/app/worker/cli_test.js` that takes a file path as an argument, reads the JSON log, runs your `classifyPayload` logic, and exits with code `0` if clean and code `1` if evil. 

Ensure everything is fully functional and the API gateway successfully routes to the worker.