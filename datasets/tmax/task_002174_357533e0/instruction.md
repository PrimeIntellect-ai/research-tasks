You are an internal web developer building a secure dependency proxy feature for our Go infrastructure. We have an internal proxy server that intercepts module requests to prevent dependency confusion and supply chain attacks.

Part 1: Fix the Vendored Package
We have a vendored proxy application located at `/app/vendored/modproxy` (version 1.2.0). However, the proxy is currently broken. It was originally designed to bind to a privileged port, but since we do not run as root, the application crashes on startup. Your first task is to fix this perturbation in `/app/vendored/modproxy/main.go` so it successfully binds to port `8080` instead when run. You must also fix the `Makefile` in that directory, which has a missing environment variable `GO111MODULE=on` preventing it from building successfully. Build the fixed proxy binary to `/home/user/modproxy-bin`.

Part 2: Build the Security Filter
You need to write a Go application at `/home/user/secfilter/main.go` that acts as a classifier for dependency requests. We have provided two directories containing JSON payloads representing incoming package requests:
- `/app/corpus/clean/`: Contains legitimate, safe package requests.
- `/app/corpus/evil/`: Contains malicious requests (typosquatting attempts, forced downgrades to vulnerable semantic versions, or invalid checksums).

Your classifier must process a directory of JSON files and output a classification log to `/home/user/classification.log`. 
For each JSON file (e.g., `req_01.json`), your program should output a single line in the format:
`[filename] : [CLEAN|EVIL]`

A request is EVIL if any of the following are true:
1. The requested semantic version is lower than the `minimum_required_version` specified in the JSON.
2. The provided `sha256_checksum` does not match the actual SHA256 hash of the `package_payload` string included in the JSON.
3. The dependency graph depth (provided as an integer `graph_depth`) exceeds 10, which we flag as an evasion tactic.

Otherwise, it is CLEAN.

Compile your classifier to `/home/user/secfilter-bin`.

Part 3: End-to-End Test Orchestration
Write a bash script at `/home/user/run_e2e.sh` that:
1. Starts the fixed `/home/user/modproxy-bin` in the background.
2. Runs your classifier against `/app/corpus/clean/` appending the results to `/home/user/classification.log`.
3. Runs your classifier against `/app/corpus/evil/` appending the results to `/home/user/classification.log`.
4. Gracefully kills the background proxy process.

Ensure all outputs are deterministic and follow the required format so our automated test suite can verify your work.