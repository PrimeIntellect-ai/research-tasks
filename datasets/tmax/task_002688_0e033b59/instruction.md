You are an open-source maintainer reviewing a pull request for `telemetry-system`, a polyglot application that processes sensor metrics. The contributor tried to add an anomaly detector and update the deployment setup, but the PR is completely broken. 

Your workspace is located at `/home/user/telemetry-system`. The system consists of three services:
1. An **Nginx** reverse proxy (needs to listen on port `8080`).
2. A **Go API backend** (listens on port `9000`).
3. A **C++ numerical worker** (listens on port `9001`).

Your goals are to fix the build orchestration, configure the proxy, implement the core anomaly detection algorithm in Go, and write a local CI script to verify it against our corpora.

### 1. Reverse Proxy Configuration
Create an Nginx configuration file at `/home/user/telemetry-system/nginx.conf`. It must:
- Run in the foreground (daemon off) or be spawnable in the background.
- Listen on port `8080`.
- Route all requests starting with `/api/` to the Go backend at `127.0.0.1:9000`.

### 2. Polyglot Build & Service Orchestration
The PR broke the startup script `/home/user/telemetry-system/start_services.sh`. Fix it so that it:
- Compiles the C++ worker (`worker.cpp`) using `g++` into an executable named `worker` and starts it on port `9001` in the background.
- Builds the Go API (`main.go`, `validator.go`) into an executable named `backend` and starts it in the background.
- Starts Nginx using the `nginx.conf` you created.

### 3. Implement the Anomaly Detector (Adversarial Corpus)
The Go backend receives JSON payloads at `POST /api/process`. The payload format is:
`{"series_a": [int, int, ...], "series_b": [int, int, ...]}`

You must implement the validation logic in `/home/user/telemetry-system/validator.go` (a skeleton is provided). The function `ValidateTelemetry(a, b []int) bool` must enforce the following rules:
1. `series_a` and `series_b` must both be **strictly monotonically increasing** (each element is strictly greater than the previous).
2. If you **merge** both series into a single sorted array, the difference between any two adjacent elements (diffing) must be **less than or equal to 10**.

If the payload violates these rules, the Go API must return HTTP status `400 Bad Request`. If it passes, return `200 OK`. 

To ensure your code is robust, we have provided two data corpora:
- **Clean Corpus**: `/home/user/telemetry-system/corpus/clean/` (Contains JSON files that MUST be accepted / return 200).
- **Evil Corpus**: `/home/user/telemetry-system/corpus/evil/` (Contains adversarial JSON files with hidden spikes, unsorted arrays, and edge cases that MUST be rejected / return 400).

### 4. CI/CD Script
Write a bash script at `/home/user/telemetry-system/ci.sh` that:
1. Starts the services by calling `start_services.sh`.
2. Iterates over all `.json` files in `/home/user/telemetry-system/corpus/clean/` and `curl`s them to `http://127.0.0.1:8080/api/process`. It must verify that EVERY clean file returns a `200` HTTP status code.
3. Iterates over all `.json` files in `/home/user/telemetry-system/corpus/evil/` and verifies that EVERY evil file returns a `400` HTTP status code.
4. If all tests pass, the script must print exactly `CI PASS` and exit with code `0`. If any fail, it must print `CI FAIL` and exit with `1`.

Your task is complete when `bash ci.sh` prints `CI PASS` and exits with code `0`.