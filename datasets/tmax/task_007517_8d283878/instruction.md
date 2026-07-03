You are acting as a capacity planner for a growing distributed storage system. We need to automate our local filesystem resource monitoring and capacity expansion pipeline. 

Your goal is to build a local health-check service in Go, an Expect script to automate an interactive allocation tool, and a mock CI/CD bash script to tie it all together.

Here are your detailed requirements:

1. **The Filesystem Health Service (Go)**
   Write a Go program located at `/home/user/fs_monitor.go`.
   - It must run an HTTP server on port `8080`.
   - It must expose a `/health` endpoint.
   - When the `/health` endpoint is queried, the program should calculate the total disk space used (in bytes) by files inside two directories: `/home/user/storage/pool1` and `/home/user/storage/pool2`.
   - If **any** of these directories contain total file sizes exceeding `10485760` bytes (10 MB), the endpoint must return an HTTP `503 Service Unavailable` status code, and the exact plain-text body: `UNHEALTHY: <pool_name>` (where `<pool_name>` is either `pool1` or `pool2`, depending on which exceeded the limit. If both exceed, returning either one is fine).
   - If both directories are strictly under 10 MB, it must return an HTTP `200 OK` status code with the body `OK`.
   - The server must also expose a reverse proxy endpoint at `/backend` that proxies requests to `http://localhost:9090` (a dummy backend, you don't need to run anything on 9090, just configure the proxy in the Go code).

2. **The Auto-Expansion Expect Script**
   There is a pre-existing interactive tool at `/home/user/tools/allocator` that manages storage quotas. It is interactive and asks three prompts:
   - `Enter pool to manage:`
   - `Select action (expand/shrink):`
   - `Confirm (y/n):`
   
   Write an Expect script at `/home/user/auto_expand.exp` that takes exactly one command-line argument (the pool name). The script must spawn `/home/user/tools/allocator`, wait for the respective prompts, and send the provided pool name, the word `expand`, and `y` to confirm.

3. **The CI/CD Automation Pipeline**
   Write a bash script at `/home/user/pipeline.sh` that represents a scheduled pipeline job.
   - It should use `curl` to query `http://localhost:8080/health`.
   - If the response is `OK`, it should do nothing and exit with code 0.
   - If the response contains `UNHEALTHY: `, it must extract the pool name from the response, and execute your Expect script `/home/user/auto_expand.exp <pool_name>`.
   - Finally, if an expansion was triggered, the pipeline script must append a line to `/home/user/capacity.log` with the exact format: `Expanded capacity for <pool_name>`.

Make sure to compile your Go program using `go build -o /home/user/fs_monitor /home/user/fs_monitor.go` and ensure `pipeline.sh` and `auto_expand.exp` are executable. Do not leave the Go server running in the foreground; we will test your compiled binary and scripts programmatically.