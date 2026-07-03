You are a Site Reliability Engineer (SRE) investigating an issue where several internal monitoring services cannot reach each other. The orchestrator's network configuration logs have been flooded with invalid or malicious route injections, causing routing table corruption. 

Your task is to build an automated, idempotent log classification and filesystem management system using only Bash. 

**Step 1: Subnet Extraction**
You have been provided with a screenshot of the original dashboard configuration at `/app/dashboard_screenshot.png`. 
Use OCR (e.g., `tesseract`) to extract the "PRIMARY SUBNET" from this image. You will need this CIDR block for the next steps.

**Step 2: Filesystem & Link Management**
Create an idempotent Bash setup script at `/home/user/setup_env.sh` that, when executed, constructs the following directory structure strictly within `/home/user/monitor_state/`:
- Directories: `active/`, `archive/`, and `quarantine/`.
- Ensure these directories have strict permissions (read/write/execute only for the owner, 0700), simulating isolated tenant environments.
- Create a symlink at `/home/user/monitor_state/latest` that points to the `active/` directory.
Your script must be fully idempotent (running it multiple times must not fail or create nested/broken links).

**Step 3: Log Classifier Script**
Write a robust Bash script at `/home/user/classify_routes.sh` to classify configuration files.
The script must take exactly one argument: the path to a log file.
`./classify_routes.sh <path_to_file>`

Each log file contains lines formatted as: `ROUTE ADD <TARGET_IP> GW <GATEWAY_IP>`

Your script must analyze the file and:
1. Validate that EVERY `<TARGET_IP>` and `<GATEWAY_IP>` in the file falls strictly within the PRIMARY SUBNET you extracted in Step 1.
2. Validate that the IPs are syntactically correct (no malformed strings).
3. If the file is 100% clean (all routes valid and within the subnet), the script must **exit with status code 0**.
4. If the file contains ANY route outside the subnet, or ANY malformed line, it must **exit with a non-zero status code** (e.g., 1).

You must use standard bash built-ins, coreutils, or standard CLI tools (like `grep`, `awk`, `sed`). Do not use Python or Perl.

An automated verifier will test your `/home/user/classify_routes.sh` script against a massive corpus of hidden clean and malicious configuration files. It must accurately accept all clean files and reject all evil files.