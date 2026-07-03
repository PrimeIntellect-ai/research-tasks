You are a Site Reliability Engineer (SRE) tasked with integrating a legacy internal component into your modern Prometheus-based monitoring stack. 

The legacy component does not have an HTTP API. Instead, it can only be queried via an interactive command-line administration tool located at `/home/user/legacy_cli.py`. 

Your objective is to write an Expect script to automate the interactive login and command execution, and then write a Go service that wraps this script to expose the health data as a Prometheus metric.

Here are the requirements:

1. **Expect Script (`/home/user/get_health.exp`)**:
   - Write an Expect script that executes `python3 /home/user/legacy_cli.py`.
   - The CLI will prompt for `Username:`. You must send `admin`.
   - It will then prompt for `Password:`. You must send `sre_admin_pass`.
   - It will then prompt for `Cmd:`. You must send `get_uptime`.
   - The CLI will output a string like `System Uptime: <number> seconds` and exit.
   - Your Expect script must print this exact output line to standard output so it can be captured.

2. **Go Monitoring Service (`/home/user/monitor.go`)**:
   - Write a Go program that sets up an HTTP server listening on `127.0.0.1:8080`.
   - Expose an endpoint at `/metrics`.
   - When `/metrics` is queried, the Go program must execute your `/home/user/get_health.exp` script, parse the standard output to extract the integer uptime value, and return it in the standard Prometheus format.
   - The exposed metric must be named exactly `legacy_service_uptime_seconds` (type gauge).
   - Example expected output of `curl http://127.0.0.1:8080/metrics`:
     ```
     # HELP legacy_service_uptime_seconds Uptime of the legacy system
     # TYPE legacy_service_uptime_seconds gauge
     legacy_service_uptime_seconds 3600
     ```

3. **Build and Run**:
   - Build your Go program into an executable named `/home/user/monitor`.
   - Run the service in the background so it is actively listening on port 8080.
   - Ensure the service is running and accessible before you finish.

Note: You can assume `expect`, `python3`, and `go` are installed. Do not hardcode the uptime value in your Go code; it must be dynamically fetched by invoking the Expect script.