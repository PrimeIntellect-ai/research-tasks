You are a mobile build engineer maintaining custom CI/CD pipelines. We need a lightweight, local WebSocket-based build coordinator backend written entirely in Bash to run on our build nodes.

Your task is to create this build coordinator by writing two files:
1. `/home/user/ci_backend.sh` (The core logic script)
2. `/home/user/start_server.sh` (A script that installs dependencies and launches the WebSocket server)

### Requirements

**1. Server Setup (`start_server.sh`)**
* Must install `websocat` and `bc` (you may use `sudo apt-get update && sudo apt-get install -y websocat bc`).
* Must start a WebSocket server on `127.0.0.1:9090`. 
* When a client connects, the server should pipe the WebSocket communication to `/home/user/ci_backend.sh` (handling stdin/stdout). Ensure the server stays alive for multiple requests (e.g., using `websocat -E ws-listen:127.0.0.1:9090 exec:/home/user/ci_backend.sh`). Run the server in the background so the script exits successfully.

**2. Core Logic (`ci_backend.sh`)**
This script will read incoming messages from standard input (one line per request) and write responses to standard output. It must handle the following sequence for each `BUILD` request:

* **Input Format**: Messages will be in the format: `BUILD <project_name> <priority_expression>`
  * Example: `BUILD AndroidApp 5+3*2`
* **Request Validation & Rate Limiting**:
  * The script must enforce a global rate limit of **2 seconds** between accepted build requests across all connections. Use `/tmp/last_build_time` to store the timestamp of the last *accepted* build.
  * If a request arrives less than 2 seconds after the last accepted build, output exactly `RATE_LIMIT` to stdout and do not process the build.
* **Expression Parsing**:
  * Evaluate the `<priority_expression>` as a mathematical expression using `bc` or Bash arithmetic.
  * If the request is accepted, immediately output: `ACCEPTED <project_name> <calculated_priority>`
* **State Machine & Logging**:
  * Upon acceptance, append `[<project_name>] INIT` to `/home/user/ci_states.log`.
  * Wait 1 second (simulating build time).
  * Append `[<project_name>] SUCCESS` to `/home/user/ci_states.log`.
* **Sorting, Merging, and Diffing**:
  * During the 1-second simulated build, read two files: `/home/user/config_base.env` and `/home/user/config_override.env` (assume these contain `KEY=VALUE` pairs).
  * Merge them such that keys in `config_override.env` replace keys in `config_base.env`. Any keys unique to either file must be kept.
  * Sort the final merged list of keys alphabetically.
  * Write the sorted, merged environment variables to `/home/user/config_merged.env`.

Make sure `/home/user/ci_backend.sh` is executable and loops continuously to process multiple lines if a client sends multiple requests in one connection.

Your tasks:
1. Write the scripts `/home/user/ci_backend.sh` and `/home/user/start_server.sh`.
2. Make them executable.
3. Execute `/home/user/start_server.sh` to leave the server running in the background.