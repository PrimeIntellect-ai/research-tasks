You have been given a legacy project in `/home/user/project` that consists of a Python 2 C-extension and a broken installation configuration. We are migrating this system to Python 3 and deploying it as part of a new CI/CD pipeline. 

The project contains the following files:
- `/home/user/project/setup.py`: A Python 2 setup script with syntax and compatibility errors.
- `/home/user/project/semver_ext.c`: A Python C-extension written for Python 2. It exposes a function `parse_and_compare(url_path, target_version)` that takes a URL path (like `/api/v1/download/1.2.3`), extracts the semantic version, and compares it against `target_version`. It relies on Python 2 C-API functions (like `PyString_AsString`, `initsemver_ext`, etc.).
- `/home/user/project/server.py`: A Python 3 standard library `http.server` that uses the `semver_ext` module to route requests and check versions. (This file is already compatible with Python 3, but cannot run until the extension is built).

Your task consists of the following phases:

**Phase 1: Migration (Python 3 & C)**
1. Modify `/home/user/project/setup.py` so that it is a valid Python 3 script.
2. Refactor `/home/user/project/semver_ext.c` to use the Python 3 C-API. You must update module initialization, method tables, and string handling (`PyUnicode_AsUTF8`, etc.). Keep the logic identical: it must extract a semver from a URL string, decode it if necessary, and return `1` if the version in the URL is greater than or equal to the target, and `0` otherwise.

**Phase 2: Concurrency & Testing (Go)**
1. Write a Go program at `/home/user/project/tester.go`. 
2. This program must read a list of URL endpoints passed as command-line arguments.
3. It must use Go concurrency (goroutines and a `sync.WaitGroup` or channels) to make HTTP GET requests to `http://127.0.0.1:8080<endpoint>` concurrently.
4. For every request that returns an HTTP 200 OK (which means the version check passed), write the endpoint string to a file `/home/user/success.log`, one per line. The order in the log file does not matter.

**Phase 3: CI/CD Setup**
1. Create a bash script at `/home/user/project/ci.sh`.
2. The script must:
   - Install the Python extension in the current environment (`python3 -m pip install .`).
   - Start the Python server (`python3 server.py`) in the background on port 8080 and wait 2 seconds for it to initialize.
   - Build the Go tester: `go build -o tester tester.go`
   - Run the Go tester with the following arguments: `/api/v1/pkg/0.9.0` `/api/v1/pkg/1.2.4` `/api/v1/pkg/2.0.0` `/api/v1/pkg/1.0.0-alpha`
   - Terminate the background Python server gracefully.
   - Exit with code 0.

Ensure that after executing `/home/user/project/ci.sh`, the file `/home/user/success.log` is generated correctly.